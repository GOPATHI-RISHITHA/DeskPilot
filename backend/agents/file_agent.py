import os
import shutil
from pathlib import Path

def create_folder(folder_path: str) -> dict:
    """Creates a folder at the specified path."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        return {"status": "success", "message": f"Folder created at: {folder_path}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to create folder: {str(e)}"}

def create_file(file_path: str, content: str = "") -> dict:
    """Creates a file with optional initial content."""
    try:
        # Ensure parent directory exists
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"File created at: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to create file: {str(e)}"}

def list_files(directory_path: str) -> dict:
    """Lists files and folders inside a given directory."""
    try:
        if not os.path.exists(directory_path):
            return {"status": "error", "message": "Directory does not exist."}

        items = os.listdir(directory_path)
        return {
            "status": "success",
            "directory": directory_path,
            "items": items
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to list directory: {str(e)}"}

def search_files(directory_path: str, keyword: str) -> dict:
    """Searches for files matching a keyword inside a directory."""
    try:
        matches = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if keyword.lower() in file.lower():
                    matches.append(os.path.join(root, file))

        return {
            "status": "success",
            "keyword": keyword,
            "matches_found": len(matches),
            "results": matches[:20]  # Return top 20 matches
        }
    except Exception as e:
        return {"status": "error", "message": f"Search failed: {str(e)}"}