from fastapi import FastAPI, HTTPException, UploadFile, File
from agents.voice_agent import transcribe_audio
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from core.ai_orchestrator import execute_user_query

from agents.application_agent import (
    open_app,
    close_app,
    list_running_apps
)

from agents.file_agent import (
    create_folder,
    create_file,
    list_files,
    search_files
)

from agents.terminal_agent import run_command

from agents.system_agent import (
    get_system_stats,
    set_volume,
    set_brightness
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="DeskPilot API",
    description="AI Operating System Assistant",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class AppRequest(BaseModel):
    app_name: str


class FolderRequest(BaseModel):
    folder_path: str


class FileRequest(BaseModel):
    file_path: str
    content: Optional[str] = ""


class SearchRequest(BaseModel):
    directory_path: str
    keyword: str


class TerminalRequest(BaseModel):
    command: str
    cwd: Optional[str] = None


class ControlRequest(BaseModel):
    level: int


class CommandRequest(BaseModel):
    command: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def read_root():

    return {
        "status": "online",
        "system": "DeskPilot Backend Active"
    }


# ============================================================
# AI COMMAND ROUTE
# ============================================================

@app.post("/api/command")
def api_execute_command(request: CommandRequest):

    try:

        print("\n========================================")
        print("DESKPILOT COMMAND")
        print("========================================")
        print(request.command)

        result = execute_user_query(
            request.command
        )

        print("\nDESKPILOT RESULT:")
        print(result)

        return {
            "status": "success",
            "command": request.command,
            "response": result
        }

    except Exception as e:

        print("\nDESKPILOT ERROR:")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# APPLICATION AGENT
# ============================================================

@app.post("/api/app/open")
def api_open_app(request: AppRequest):

    result = open_app(
        request.app_name
    )

    if result.get("status") == "error":

        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    return result


@app.post("/api/app/close")
def api_close_app(request: AppRequest):

    return close_app(
        request.app_name
    )


@app.get("/api/app/running")
def api_list_running():

    return list_running_apps()


# ============================================================
# FILE AGENT
# ============================================================

@app.post("/api/file/create-folder")
def api_create_folder(request: FolderRequest):

    return create_folder(
        request.folder_path
    )


@app.post("/api/file/create-file")
def api_create_file(request: FileRequest):

    return create_file(
        request.file_path,
        request.content
    )


@app.post("/api/file/list")
def api_list_files(request: FolderRequest):

    return list_files(
        request.folder_path
    )


@app.post("/api/file/search")
def api_search_files(request: SearchRequest):

    return search_files(
        request.directory_path,
        request.keyword
    )


# ============================================================
# TERMINAL AGENT
# ============================================================

@app.post("/api/terminal/run")
def api_run_terminal(request: TerminalRequest):

    return run_command(
        request.command,
        request.cwd
    )


# ============================================================
# SYSTEM AGENT
# ============================================================

@app.get("/api/system/stats")
def api_get_stats():

    return get_system_stats()


@app.post("/api/system/volume")
def api_set_volume(request: ControlRequest):

    return set_volume(
        request.level
    )


@app.post("/api/system/brightness")
def api_set_brightness(request: ControlRequest):

    return set_brightness(
        request.level
    )
@app.post("/api/voice")
async def api_voice_command(audio: UploadFile = File(...)):
    """
    Receives microphone audio, converts it to text,
    then sends the transcript to the DeskPilot AI orchestrator.
    """

    try:

        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="No audio data received."
            )

        # ---------------------------------------------
        # Speech → Text
        # ---------------------------------------------

        transcription = transcribe_audio(
            audio_bytes,
            audio.content_type or "audio/webm"
        )

        if transcription.get("status") != "success":

            raise HTTPException(
                status_code=500,
                detail=transcription.get(
                    "message",
                    "Voice transcription failed."
                )
            )

        transcript = transcription["transcript"]

        if not transcript:

            raise HTTPException(
                status_code=400,
                detail="Could not understand the voice command."
            )

        # ---------------------------------------------
        # Text → Gemini → Tools → Action
        # ---------------------------------------------

        result = execute_user_query(transcript)

        return {
            "status": "success",
            "transcript": transcript,
            "response": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )