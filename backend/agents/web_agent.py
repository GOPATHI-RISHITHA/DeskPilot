import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# LOAD API KEY
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found. Please add GEMINI_API_KEY to backend/.env"
    )


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# WEB RESEARCH TOOL
# ---------------------------------------------------------

def web_research(topic: str) -> dict:
    """
    Searches the web using Gemini Google Search grounding
    and returns useful researched content.
    """

    try:

        prompt = f"""
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

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
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

        # -------------------------------------------------
        # EXTRACT SOURCES
        # -------------------------------------------------

        sources = []

        try:

            grounding_metadata = response.candidates[0].grounding_metadata

            if grounding_metadata and grounding_metadata.grounding_chunks:

                for chunk in grounding_metadata.grounding_chunks:

                    if hasattr(chunk, "web") and chunk.web:

                        uri = getattr(chunk.web, "uri", None)
                        title = getattr(chunk.web, "title", None)

                        if uri:

                            sources.append({
                                "title": title or "Web source",
                                "url": uri
                            })

        except Exception:
            pass


        return {
            "status": "success",
            "topic": topic,
            "content": content,
            "sources": sources
        }


    except Exception as e:

        return {
            "status": "error",
            "message": f"Web research failed: {str(e)}"
        }