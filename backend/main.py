from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import agents
from agents.application_agent import open_app, close_app, list_running_apps
from agents.file_agent import create_folder, create_file, list_files, search_files
from agents.terminal_agent import run_command
from agents.system_agent import get_system_stats, set_volume, set_brightness

app = FastAPI(
    title="DeskPilot API",
    description="AI Operating System Assistant",
    version="1.0"
)

# Configure CORS Middleware to allow browser / Swagger UI communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Request Schemas
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
    level: int  # Value between 0 and 100

@app.get("/")
def read_root():
    return {"status": "online", "system": "DeskPilot Backend Active"}

# ----------------------------
# 1. Application Agent Routes
# ----------------------------
@app.post("/api/app/open")
def api_open_app(request: AppRequest):
    result = open_app(request.app_name)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/app/close")
def api_close_app(request: AppRequest):
    return close_app(request.app_name)

@app.get("/api/app/running")
def api_list_running():
    return list_running_apps()

# ----------------------------
# 2. File Agent Routes
# ----------------------------
@app.post("/api/file/create-folder")
def api_create_folder(request: FolderRequest):
    return create_folder(request.folder_path)

@app.post("/api/file/create-file")
def api_create_file(request: FileRequest):
    return create_file(request.file_path, request.content)

@app.post("/api/file/list")
def api_list_files(request: FolderRequest):
    return list_files(request.folder_path)

@app.post("/api/file/search")
def api_search_files(request: SearchRequest):
    return search_files(request.directory_path, request.keyword)

# ----------------------------
# 3. Terminal Agent Routes
# ----------------------------
@app.post("/api/terminal/run")
def api_run_terminal(request: TerminalRequest):
    return run_command(request.command, request.cwd)

# ----------------------------
# 4. System Agent Routes
# ----------------------------
@app.get("/api/system/stats")
def api_get_stats():
    return get_system_stats()

@app.post("/api/system/volume")
def api_set_volume(request: ControlRequest):
    return set_volume(request.level)

@app.post("/api/system/brightness")
def api_set_brightness(request: ControlRequest):
    return set_brightness(request.level)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)