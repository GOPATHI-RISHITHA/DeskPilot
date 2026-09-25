import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD GEMINI API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found. "
        "Please add GEMINI_API_KEY to backend/.env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


# ============================================================
# RESEARCH PROMPT
# ============================================================

def build_research_prompt(topic: str) -> str:

    return f"""
Research the following topic from reliable web sources:

{topic}

Create concise but useful study notes.

Requirements:

1. Focus on important concepts.
2. Prefer reliable educational and technical sources.
3. Explain concepts in simple language.
4. Include important definitions.
5. Include important examples where useful.
6. Include commonly asked placement/interview points.
7. Include important differences or comparisons.
8. Do not include unnecessary information.
9. Organize the answer with headings and bullet points.
10. The result should be suitable for saving into a study notes file.

Do not mention that you are an AI.
"""


# ============================================================
# FALLBACK PROMPT
# ============================================================

def build_fallback_prompt(topic: str) -> str:

    return f"""
Provide useful study notes about the following topic using
your built-in knowledge:

{topic}

The normal web-research service is temporarily unavailable,
so answer directly using your existing knowledge.

Requirements:

1. Focus on important concepts.
2. Explain concepts in simple language.
3. Include important definitions.
4. Include important examples where useful.
5. Include commonly asked placement/interview points.
6. Include important differences or comparisons.
7. Do not include unnecessary information.
8. Organize the answer with headings and bullet points.
9. Make the content suitable for saving into a study notes file.
10. Do not claim that you searched the web.
11. Do not invent web sources or URLs.

Do not mention that you are an AI.
"""


# ============================================================
# CHECK WHETHER ERROR IS RELATED TO RATE LIMIT / QUOTA
# ============================================================

def is_rate_limit_error(error: Exception) -> bool:

    error_text = str(error).lower()

    rate_limit_keywords = [
        "429",
        "rate limit",
        "rate-limit",
        "quota",
        "resource exhausted",
        "too many requests",
        "limit exceeded",
        "resource_exhausted",
    ]

    return any(
        keyword in error_text
        for keyword in rate_limit_keywords
    )


# ============================================================
# EXTRACT WEB SOURCES
# ============================================================

def extract_sources(response) -> list:

    sources = []

    try:

        grounding_metadata = (
            response.candidates[0].grounding_metadata
        )

        if (
            grounding_metadata
            and grounding_metadata.grounding_chunks
        ):

            for chunk in grounding_metadata.grounding_chunks:

                if hasattr(chunk, "web") and chunk.web:

                    uri = getattr(
                        chunk.web,
                        "uri",
                        None
                    )

                    title = getattr(
                        chunk.web,
                        "title",
                        None
                    )

                    if uri:

                        sources.append(
                            {
                                "title": (
                                    title
                                    or "Web source"
                                ),
                                "url": uri,
                            }
                        )

    except Exception:
        pass

    return sources


# ============================================================
# WEB RESEARCH
# ============================================================

def web_research(topic: str) -> dict:

    # --------------------------------------------------------
    # STEP 1 — TRY REAL WEB RESEARCH
    # --------------------------------------------------------

    try:

        prompt = build_research_prompt(topic)

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(

                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]

            )

        )

        content = response.text

        sources = extract_sources(response)

        return {

            "status": "success",

            "topic": topic,

            "content": content,

            "sources": sources,

            "source_type": "web",

            "fallback_used": False,

        }


    except Exception as web_error:

        print(
            "\n================================================"
        )

        print("WEB RESEARCH FAILED")

        print(web_error)

        print(
            "================================================"
        )


        # ----------------------------------------------------
        # STEP 2 — AUTOMATIC FALLBACK
        # ----------------------------------------------------

        if is_rate_limit_error(web_error):

            print(
                "Web research rate limit detected."
            )

            print(
                "Switching automatically to Gemini "
                "built-in knowledge..."
            )

        else:

            print(
                "Web research unavailable."
            )

            print(
                "Trying Gemini built-in knowledge "
                "as fallback..."
            )


        try:

            fallback_prompt = build_fallback_prompt(
                topic
            )

            fallback_response = (
                client.models.generate_content(

                    model=MODEL_NAME,

                    contents=fallback_prompt,

                )
            )

            fallback_content = (
                fallback_response.text
            )

            return {

                "status": "success",

                "topic": topic,

                "content": fallback_content,

                "sources": [],

                "source_type": "gemini_knowledge",

                "fallback_used": True,

                "message": (
                    "Web research was unavailable. "
                    "DeskPilot automatically used "
                    "Gemini's built-in knowledge."
                ),

            }


        except Exception as fallback_error:

            print(
                "\n================================================"
            )

            print("GEMINI FALLBACK ALSO FAILED")

            print(fallback_error)

            print(
                "================================================"
            )

            return {

                "status": "error",

                "topic": topic,

                "message": (
                    "Web research and automatic "
                    "Gemini fallback both failed: "
                    f"{fallback_error}"
                ),

                "fallback_used": True,

            }