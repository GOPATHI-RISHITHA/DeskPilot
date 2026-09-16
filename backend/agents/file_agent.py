import os
import shutil
import subprocess
from pathlib import Path


# =========================================================
# WINDOWS SPECIAL FOLDER HELPERS
# =========================================================

def get_desktop_path() -> str:
    """
    Returns the actual Windows Desktop path.

    This works even when Desktop is redirected to OneDrive.
    """

    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "[Environment]::GetFolderPath('Desktop')"
            ],
            text=True
        ).strip()

        if result:
            return result

    except Exception:
        pass

    # Fallback
    return os.path.join(
        os.environ.get("USERPROFILE", ""),
        "Desktop"
    )


def resolve_path(path: str) -> str:
    """
    Converts user-friendly paths into real Windows paths.

    Examples:

    Desktop
    Desktop/Study
    Desktop/Study/DBMS.txt
    Study
    Study/DBMS.txt
    """

    path = path.strip()

    # Remove quotes
    path = path.strip('"').strip("'")

    desktop = get_desktop_path()

    # -----------------------------------------------------
    # Desktop paths
    # -----------------------------------------------------

    if path.lower() == "desktop":
        return desktop

    if path.lower().startswith("desktop\\") or \
       path.lower().startswith("desktop/"):

        relative = path[8:].lstrip("\\/")
        return os.path.join(desktop, relative)

    # -----------------------------------------------------
    # Study folder
    #
    # If Gemini gives "Study/DBMS.txt", interpret Study
    # as a folder on the user's Desktop.
    # -----------------------------------------------------

    if path.lower() == "study":
        return os.path.join(desktop, "Study")

    if path.lower().startswith("study\\") or \
       path.lower().startswith("study/"):

        relative = path[6:].lstrip("\\/")
        return os.path.join(desktop, "Study", relative)

    # -----------------------------------------------------
    # Already absolute path
    # -----------------------------------------------------

    if os.path.isabs(path):
        return path

    # -----------------------------------------------------
    # Other relative paths
    # Put them on Desktop.
    # -----------------------------------------------------

    return os.path.join(desktop, path)


# =========================================================
# CREATE FOLDER
# =========================================================

def create_folder(folder_path: str) -> dict:
    """
    Creates a folder.

    User-friendly paths such as:
    Desktop/Study
    Study
    Study/DBMS
    are automatically resolved to the real Desktop.
    """

    try:

        actual_path = resolve_path(folder_path)

        os.makedirs(actual_path, exist_ok=True)

        return {
            "status": "success",
            "message": f"Folder created successfully at: {actual_path}",
            "path": actual_path
        }

    except Exception as e:

        return {
            "status": "error",
            "message": f"Failed to create folder: {str(e)}"
        }


# =========================================================
# CREATE FILE
# =========================================================

def create_file(file_path: str, content: str = "") -> dict:
    """
    Creates a file with optional content.

    User-friendly paths are automatically resolved.
    """

    try:

        actual_path = resolve_path(file_path)

        parent_dir = os.path.dirname(actual_path)

        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(actual_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "message": f"File created successfully at: {actual_path}",
            "path": actual_path
        }

    except Exception as e:

        return {
            "status": "error",
            "message": f"Failed to create file: {str(e)}"
        }


# =========================================================
# LIST FILES
# =========================================================

def list_files(directory_path: str) -> dict:
    """
    Lists files and folders inside a directory.
    """

    try:

        actual_path = resolve_path(directory_path)

        if not os.path.exists(actual_path):
            return {
                "status": "error",
                "message": f"Directory does not exist: {actual_path}"
            }

        items = os.listdir(actual_path)

        return {
            "status": "success",
            "directory": actual_path,
            "items": items
        }

    except Exception as e:

        return {
            "status": "error",
            "message": f"Failed to list directory: {str(e)}"
        }


# =========================================================
# SEARCH FILES
# =========================================================

def search_files(directory_path: str, keyword: str) -> dict:
    """
    Searches for files matching a keyword.
    """

    try:

        actual_path = resolve_path(directory_path)

        if not os.path.exists(actual_path):
            return {
                "status": "error",
                "message": f"Directory does not exist: {actual_path}"
            }

        matches = []

        for root, _, files in os.walk(actual_path):

            for file in files:

                if keyword.lower() in file.lower():

                    matches.append(
                        os.path.join(root, file)
                    )

        return {
            "status": "success",
            "keyword": keyword,
            "matches_found": len(matches),
            "results": matches[:20]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": f"Search failed: {str(e)}"
        }