import os
import tempfile

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found. Please add GEMINI_API_KEY to backend/.env"
    )

client = genai.Client(api_key=api_key)


def transcribe_audio(audio_bytes: bytes, mime_type: str = "audio/webm") -> dict:
    temp_path = None

    try:
        # Decide file extension
        extension = ".webm"

        if "wav" in mime_type:
            extension = ".wav"
        elif "mp3" in mime_type:
            extension = ".mp3"
        elif "ogg" in mime_type:
            extension = ".ogg"
        elif "m4a" in mime_type or "x-m4a" in mime_type:
            extension = ".m4a"

        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        print("Audio saved temporarily:", temp_path)
        print("Audio MIME type:", mime_type)

        # Upload audio to Gemini
        audio_file = client.files.upload(file=temp_path)

        # Ask Gemini to transcribe the recording
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[
                audio_file,
                """
Transcribe the spoken audio accurately.

Return ONLY the words spoken by the user.

Do not explain.
Do not summarize.
Do not add quotation marks.

IMPORTANT EMAIL RULES:
- If the user speaks an email address, preserve it exactly.
- Never convert an email address into a person's name.
- Never replace an email address with a contact name.
- Preserve the username, @ symbol, domain, and dots.
- If the user clearly says "at" and "dot" while spelling an email
  address, convert them to @ and . respectively.
- Do not autocorrect or guess an email address.

Example:
If the user says:
rishithagopathi@gmail.com

The transcription MUST be:
rishithagopathi@gmail.com

NOT:
Rishitha Gupati@gmail.com

Preserve technical terms such as:
DBMS, SQL, Java, Python, GitHub, VS Code,
Docker, Spring Boot, PostgreSQL, React, API.

The transcription will be used as a computer command.
"""
            ]
        )

        # Safely extract text
        transcript = ""

        if response.text:
            transcript = response.text.strip()

        # Fallback: extract text from response parts
        if not transcript and response.candidates:
            try:
                parts = response.candidates[0].content.parts

                text_parts = []

                for part in parts:
                    if getattr(part, "text", None):
                        text_parts.append(part.text)

                transcript = " ".join(text_parts).strip()

            except Exception as extraction_error:
                print(
                    "Could not extract text from response:",
                    extraction_error
                )

        if not transcript:
            return {
                "status": "error",
                "message": "Gemini did not return a transcription."
            }

        print("Transcript:", transcript)

        return {
            "status": "success",
            "transcript": transcript
        }

    except Exception as e:

        print("Voice transcription error:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }

    finally:

        # Delete temporary audio file
        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)

            except Exception:
                pass