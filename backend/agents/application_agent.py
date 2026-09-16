import os
import subprocess
import psutil
import shutil
import json
from pathlib import Path


# ============================================================
# APPLICATION MAP
# ============================================================

APP_MAP = {

    # --------------------------------------------------------
    # Browsers
    # --------------------------------------------------------

    "edge": "msedge",
    "msedge": "msedge",
    "microsoft edge": "msedge",
    "microsoft-edge": "msedge",

    "chrome": "chrome",
    "google chrome": "chrome",
    "google-chrome": "chrome",

    "brave": "brave",
    "brave browser": "brave",

    "firefox": "firefox",
    "mozilla firefox": "firefox",

    # --------------------------------------------------------
    # Editors / IDEs
    # --------------------------------------------------------

    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "code": "code",

    "notepad": "notepad",

    # --------------------------------------------------------
    # Windows utilities
    # --------------------------------------------------------

    "paint": "mspaint",
    "mspaint": "mspaint",
    "microsoft paint": "mspaint",

    "calculator": "__calculator__",
    "calc": "__calculator__",
    "windows calculator": "__calculator__",

    "cmd": "cmd",
    "command prompt": "cmd",

    "powershell": "powershell",
    "power shell": "powershell",
    "windows powershell": "powershell",

    "explorer": "explorer",
    "file explorer": "explorer",
    "windows explorer": "explorer",

    "settings": "ms-settings:",
    "windows settings": "ms-settings:",

    "task manager": "taskmgr",
    "taskmanager": "taskmgr",

    "control panel": "control",
    "controlpanel": "control",

    # --------------------------------------------------------
    # Other applications
    # --------------------------------------------------------

    "spotify": "spotify:",
    "whatsapp": "whatsapp:",
    "discord": "discord",
}


# ============================================================
# PROCESS MAP
# ============================================================

PROCESS_MAP = {

    "vscode": "Code.exe",
    "vs code": "Code.exe",
    "visual studio code": "Code.exe",
    "code": "Code.exe",

    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "google-chrome": "chrome.exe",

    "edge": "msedge.exe",
    "msedge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "microsoft-edge": "msedge.exe",

    "firefox": "firefox.exe",
    "mozilla firefox": "firefox.exe",

    "brave": "brave.exe",
    "brave browser": "brave.exe",

    "notepad": "notepad.exe",

    "paint": "mspaint.exe",
    "mspaint": "mspaint.exe",
    "microsoft paint": "mspaint.exe",

    "calculator": "CalculatorApp.exe",
    "calc": "CalculatorApp.exe",
    "windows calculator": "CalculatorApp.exe",

    "spotify": "Spotify.exe",

    "discord": "Discord.exe",
}


# ============================================================
# DESKTOP PATH
# ============================================================

def get_desktop_path():
    """
    Get the actual Windows Desktop path.

    Works with normal Desktop and OneDrive Desktop.
    """

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "[Environment]::GetFolderPath('Desktop')"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        desktop = result.stdout.strip()

        if desktop and os.path.isdir(desktop):
            return Path(desktop)

    except Exception:
        pass

    return Path.home() / "Desktop"


# ============================================================
# DOCUMENTS PATH
# ============================================================

def get_documents_path():
    """
    Get the actual Windows Documents path.
    """

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "[Environment]::GetFolderPath('MyDocuments')"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        documents = result.stdout.strip()

        if documents and os.path.isdir(documents):
            return Path(documents)

    except Exception:
        pass

    return Path.home() / "Documents"


# ============================================================
# DOWNLOADS PATH
# ============================================================

def get_downloads_path():

    downloads = Path.home() / "Downloads"

    if downloads.exists():
        return downloads

    return None


# ============================================================
# RESOLVE KNOWN PATH
# ============================================================

def resolve_known_path(name: str):
    """
    Resolve common natural-language paths.

    Examples:

        Study
        Desktop
        Desktop/Study
        Study/DBMS.pdf
        Documents
        Downloads
    """

    clean_name = (
        name
        .strip()
        .strip('"')
        .strip("'")
    )

    if not clean_name:
        return None

    desktop = get_desktop_path()
    documents = get_documents_path()
    downloads = get_downloads_path()

    # --------------------------------------------------------
    # Absolute path
    # --------------------------------------------------------

    path = Path(clean_name)

    if path.is_absolute() and path.exists():
        return path

    # --------------------------------------------------------
    # Desktop
    # --------------------------------------------------------

    if clean_name.lower() in [
        "desktop",
        "my desktop"
    ]:
        return desktop

    # --------------------------------------------------------
    # Documents
    # --------------------------------------------------------

    if clean_name.lower() in [
        "documents",
        "my documents"
    ]:
        return documents

    # --------------------------------------------------------
    # Downloads
    # --------------------------------------------------------

    if downloads and clean_name.lower() in [
        "downloads",
        "my downloads"
    ]:
        return downloads

    # --------------------------------------------------------
    # Remove "my" and "the"
    # --------------------------------------------------------

    normalized = clean_name

    if normalized.lower().startswith("my "):
        normalized = normalized[3:]

    if normalized.lower().startswith("the "):
        normalized = normalized[4:]

    lower = normalized.lower()

    # --------------------------------------------------------
    # Desktop/...
    # --------------------------------------------------------

    if lower.startswith("desktop\\"):

        relative = normalized[8:]

        candidate = desktop / relative

        if candidate.exists():
            return candidate

    if lower.startswith("desktop/"):

        relative = normalized[8:]

        candidate = desktop / relative

        if candidate.exists():
            return candidate

    # --------------------------------------------------------
    # Study
    # --------------------------------------------------------

    if lower == "study":

        candidate = desktop / "Study"

        if candidate.exists():
            return candidate

    if lower.startswith("study\\"):

        relative = normalized[6:]

        candidate = desktop / "Study" / relative

        if candidate.exists():
            return candidate

    if lower.startswith("study/"):

        relative = normalized[6:]

        candidate = desktop / "Study" / relative

        if candidate.exists():
            return candidate

    # --------------------------------------------------------
    # Documents/...
    # --------------------------------------------------------

    if lower.startswith("documents\\"):

        relative = normalized[10:]

        candidate = documents / relative

        if candidate.exists():
            return candidate

    if lower.startswith("documents/"):

        relative = normalized[10:]

        candidate = documents / relative

        if candidate.exists():
            return candidate

    # --------------------------------------------------------
    # Downloads/...
    # --------------------------------------------------------

    if downloads:

        if lower.startswith("downloads\\"):

            relative = normalized[10:]

            candidate = downloads / relative

            if candidate.exists():
                return candidate

        if lower.startswith("downloads/"):

            relative = normalized[10:]

            candidate = downloads / relative

            if candidate.exists():
                return candidate

    # --------------------------------------------------------
    # Directly inside Desktop
    # --------------------------------------------------------

    candidate = desktop / normalized

    if candidate.exists():
        return candidate

    # --------------------------------------------------------
    # Directly inside Documents
    # --------------------------------------------------------

    candidate = documents / normalized

    if candidate.exists():
        return candidate

    # --------------------------------------------------------
    # Directly inside Downloads
    # --------------------------------------------------------

    if downloads:

        candidate = downloads / normalized

        if candidate.exists():
            return candidate

    return None


# ============================================================
# SEARCH USER FILE / FOLDER
# ============================================================

def search_user_file(name: str):
    """
    Search Desktop, Documents, Study and Downloads.

    Used when the user asks to open a file/folder
    that is not directly resolved.
    """

    clean_name = (
        name
        .strip()
        .strip('"')
        .strip("'")
    )

    if not clean_name:
        return None

    desktop = get_desktop_path()
    documents = get_documents_path()
    downloads = get_downloads_path()

    search_locations = [
        desktop,
        documents,
        desktop / "Study"
    ]

    if downloads:
        search_locations.append(downloads)

    # --------------------------------------------------------
    # Remove duplicate/non-existing locations
    # --------------------------------------------------------

    unique_locations = []

    for location in search_locations:

        if (
            location.exists()
            and location not in unique_locations
        ):
            unique_locations.append(location)

    # --------------------------------------------------------
    # Exact name
    # --------------------------------------------------------

    for location in unique_locations:

        try:

            for item in location.rglob("*"):

                if item.name.lower() == clean_name.lower():
                    return item

        except (
            PermissionError,
            OSError
        ):
            continue

    # --------------------------------------------------------
    # Match filename without extension
    # --------------------------------------------------------

    clean_stem = Path(clean_name).stem.lower()

    for location in unique_locations:

        try:

            for item in location.rglob("*"):

                if item.stem.lower() == clean_stem:
                    return item

        except (
            PermissionError,
            OSError
        ):
            continue

    # --------------------------------------------------------
    # Partial match
    # --------------------------------------------------------

    for location in unique_locations:

        try:

            for item in location.rglob("*"):

                if clean_stem in item.stem.lower():
                    return item

        except (
            PermissionError,
            OSError
        ):
            continue

    return None


# ============================================================
# OPEN WINDOWS INSTALLED APP
# ============================================================

def open_windows_app(app_name: str) -> dict:
    """
    Find an installed Windows application using
    the Windows Start Menu application list.
    """

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "Get-StartApps | ConvertTo-Json -Compress"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:

            return {
                "status": "error",
                "message": "Could not read Windows applications."
            }

        output = result.stdout.strip()

        if not output:

            return {
                "status": "error",
                "message": "No Windows applications found."
            }

        apps = json.loads(output)

        if isinstance(apps, dict):
            apps = [apps]

        requested = (
            app_name
            .lower()
            .strip()
        )

        selected = None

        # ----------------------------------------------------
        # Exact match
        # ----------------------------------------------------

        for app in apps:

            name = str(
                app.get("Name", "")
            ).lower().strip()

            if name == requested:

                selected = app
                break

        # ----------------------------------------------------
        # Partial match
        # ----------------------------------------------------

        if selected is None:

            for app in apps:

                name = str(
                    app.get("Name", "")
                ).lower().strip()

                if requested in name:

                    selected = app
                    break

        if selected is None:

            return {
                "status": "error",
                "message": (
                    f"Windows app '{app_name}' "
                    f"was not found."
                )
            }

        app_id = selected.get("AppID")

        if not app_id:

            return {
                "status": "error",
                "message": (
                    f"No AppID found for {app_name}."
                )
            }

        subprocess.Popen(
            [
                "explorer.exe",
                f"shell:AppsFolder\\{app_id}"
            ],
            shell=False
        )

        return {
            "status": "success",
            "message": (
                f"Opened {selected['Name']} successfully."
            )
        }

    except json.JSONDecodeError:

        return {
            "status": "error",
            "message": (
                "Could not read the Windows "
                "application list."
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": (
                f"Failed to open {app_name}: {str(e)}"
            )
        }


# ============================================================
# OPEN FILE / FOLDER
# ============================================================

def open_path(path: Path):
    """
    Open a real Windows file or folder.
    """

    try:

        if not path.exists():

            return {
                "status": "error",
                "message": (
                    f"Path does not exist: {path}"
                )
            }

        os.startfile(str(path))

        return {
            "status": "success",
            "message": (
                f"Opened {path.name} successfully."
            ),
            "path": str(path)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": (
                f"Failed to open {path}: {str(e)}"
            )
        }


# ============================================================
# LAUNCH APPLICATION
# ============================================================

def launch_application(
    target: str,
    original_name: str
):
    """
    Launch Windows applications reliably.

    Order:

        1. Special applications
        2. Protocol applications
        3. Executable in PATH
        4. Common installation locations
        5. Windows Start Menu applications
        6. Direct executable fallback
    """

    try:

        # ====================================================
        # CALCULATOR
        # ====================================================

        if target == "__calculator__":

            subprocess.Popen(
                ["calc.exe"],
                shell=False
            )

            return {
                "status": "success",
                "message": (
                    "Opened Calculator successfully."
                )
            }

        # ====================================================
        # PROTOCOL APPLICATION
        # ====================================================

        if target.endswith(":"):

            subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    f"Start-Process '{target}'"
                ],
                shell=False
            )

            return {
                "status": "success",
                "message": (
                    f"Opened {original_name} successfully."
                )
            }

        # ====================================================
        # EXECUTABLE IN PATH
        # ====================================================

        executable = shutil.which(target)

        if executable:

            subprocess.Popen(
                [executable],
                shell=False
            )

            return {
                "status": "success",
                "message": (
                    f"Opened {original_name} successfully."
                )
            }

        # ====================================================
        # GOOGLE CHROME
        # ====================================================

        if target.lower() == "chrome":

            chrome_paths = [

                # Program Files
                Path(
                    os.environ.get(
                        "PROGRAMFILES",
                        r"C:\Program Files"
                    )
                )
                / "Google"
                / "Chrome"
                / "Application"
                / "chrome.exe",

                # Program Files (x86)
                Path(
                    os.environ.get(
                        "PROGRAMFILES(X86)",
                        r"C:\Program Files (x86)"
                    )
                )
                / "Google"
                / "Chrome"
                / "Application"
                / "chrome.exe",

                # Local AppData
                Path(
                    os.environ.get(
                        "LOCALAPPDATA",
                        ""
                    )
                )
                / "Google"
                / "Chrome"
                / "Application"
                / "chrome.exe",

            ]

            for chrome_path in chrome_paths:

                if chrome_path.exists():

                    subprocess.Popen(
                        [str(chrome_path)],
                        shell=False
                    )

                    return {
                        "status": "success",
                        "message": (
                            f"Opened {original_name} "
                            f"successfully."
                        )
                    }

        # ====================================================
        # MICROSOFT EDGE
        # ====================================================

        if target.lower() == "msedge":

            edge_paths = [

                # Program Files
                Path(
                    os.environ.get(
                        "PROGRAMFILES",
                        r"C:\Program Files"
                    )
                )
                / "Microsoft"
                / "Edge"
                / "Application"
                / "msedge.exe",

                # Program Files (x86)
                Path(
                    os.environ.get(
                        "PROGRAMFILES(X86)",
                        r"C:\Program Files (x86)"
                    )
                )
                / "Microsoft"
                / "Edge"
                / "Application"
                / "msedge.exe",

                # Local AppData
                Path(
                    os.environ.get(
                        "LOCALAPPDATA",
                        ""
                    )
                )
                / "Microsoft"
                / "Edge"
                / "Application"
                / "msedge.exe",

            ]

            for edge_path in edge_paths:

                if edge_path.exists():

                    subprocess.Popen(
                        [str(edge_path)],
                        shell=False
                    )

                    return {
                        "status": "success",
                        "message": (
                            f"Opened {original_name} "
                            f"successfully."
                        )
                    }

        # ====================================================
        # BRAVE BROWSER
        # ====================================================

        if target.lower() == "brave":

            brave_paths = [

                Path(
                    os.environ.get(
                        "PROGRAMFILES",
                        r"C:\Program Files"
                    )
                )
                / "BraveSoftware"
                / "Brave-Browser"
                / "Application"
                / "brave.exe",

                Path(
                    os.environ.get(
                        "PROGRAMFILES(X86)",
                        r"C:\Program Files (x86)"
                    )
                )
                / "BraveSoftware"
                / "Brave-Browser"
                / "Application"
                / "brave.exe",

                Path(
                    os.environ.get(
                        "LOCALAPPDATA",
                        ""
                    )
                )
                / "BraveSoftware"
                / "Brave-Browser"
                / "Application"
                / "brave.exe",

            ]

            for brave_path in brave_paths:

                if brave_path.exists():

                    subprocess.Popen(
                        [str(brave_path)],
                        shell=False
                    )

                    return {
                        "status": "success",
                        "message": (
                            f"Opened {original_name} "
                            f"successfully."
                        )
                    }

        # ====================================================
        # FIREFOX
        # ====================================================

        if target.lower() == "firefox":

            firefox_paths = [

                Path(
                    os.environ.get(
                        "PROGRAMFILES",
                        r"C:\Program Files"
                    )
                )
                / "Mozilla Firefox"
                / "firefox.exe",

                Path(
                    os.environ.get(
                        "PROGRAMFILES(X86)",
                        r"C:\Program Files (x86)"
                    )
                )
                / "Mozilla Firefox"
                / "firefox.exe",

            ]

            for firefox_path in firefox_paths:

                if firefox_path.exists():

                    subprocess.Popen(
                        [str(firefox_path)],
                        shell=False
                    )

                    return {
                        "status": "success",
                        "message": (
                            f"Opened {original_name} "
                            f"successfully."
                        )
                    }

        # ====================================================
        # WINDOWS INSTALLED APPLICATIONS
        # ====================================================

        windows_result = open_windows_app(
            original_name
        )

        if windows_result["status"] == "success":

            return windows_result

        # ====================================================
        # DIRECT WINDOWS EXECUTABLE
        # ====================================================

        try:

            subprocess.Popen(
                [target],
                shell=False
            )

            return {
                "status": "success",
                "message": (
                    f"Opened {original_name} "
                    f"successfully."
                )
            }

        except FileNotFoundError:

            pass

        # ====================================================
        # ERROR
        # ====================================================

        return {
            "status": "error",
            "message": (
                f"Could not find the application "
                f"'{original_name}'."
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": (
                f"Failed to open "
                f"{original_name}: {str(e)}"
            )
        }


# ============================================================
# SMART OPEN
# ============================================================

def open_app(app_name: str) -> dict:
    """
    Smart opener for:

        Applications
        Files
        Folders
        Windows Store apps
    """

    clean_name = (
        app_name
        .lower()
        .strip()
        .strip('"')
        .strip("'")
    )

    if not clean_name:

        return {
            "status": "error",
            "message": (
                "No application, file, "
                "or folder name was provided."
            )
        }

    # ========================================================
    # STEP 1 — KNOWN APPLICATIONS FIRST
    #
    # IMPORTANT:
    # This happens BEFORE file searching.
    #
    # This prevents a file such as:
    #
    # calculator.js
    #
    # from being opened when the user means Calculator.
    # ========================================================

    if clean_name in APP_MAP:

        target = APP_MAP[clean_name]

        return launch_application(
            target,
            app_name
        )

    # ========================================================
    # STEP 2 — REAL KNOWN FILE / FOLDER PATH
    # ========================================================

    resolved_path = resolve_known_path(app_name)

    if resolved_path:

        return open_path(resolved_path)

    # ========================================================
    # STEP 3 — WINDOWS INSTALLED APPLICATIONS
    # ========================================================

    windows_result = open_windows_app(app_name)

    if windows_result["status"] == "success":

        return windows_result

    # ========================================================
    # STEP 4 — SEARCH FOR FILE / FOLDER
    # ========================================================

    found_path = search_user_file(app_name)

    if found_path:

        return open_path(found_path)

    # ========================================================
    # STEP 5 — TRY AS DIRECT EXECUTABLE
    # ========================================================

    return launch_application(
        clean_name,
        app_name
    )


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_app(app_name: str) -> dict:
    """
    Close a running application.
    """

    clean_name = (
        app_name
        .lower()
        .strip()
        .strip('"')
        .strip("'")
    )

    process_exe = PROCESS_MAP.get(
        clean_name,
        f"{clean_name}.exe"
    )

    closed = False

    for proc in psutil.process_iter(["name"]):

        try:

            process_name = proc.info["name"]

            if (
                process_name
                and process_name.lower()
                == process_exe.lower()
            ):

                proc.kill()

                closed = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue

    if closed:

        return {
            "status": "success",
            "message": (
                f"Closed {app_name} successfully."
            )
        }

    return {
        "status": "warning",
        "message": (
            f"No running process found "
            f"for {app_name}."
        )
    }


# ============================================================
# LIST RUNNING APPLICATIONS
# ============================================================

def list_running_apps() -> dict:
    """
    List running Windows processes.
    """

    running = []

    for proc in psutil.process_iter(["name"]):

        try:

            process_name = proc.info["name"]

            if (
                process_name
                and process_name not in running
            ):

                running.append(process_name)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue

    return {
        "status": "success",
        "running_processes_count": len(running)
    }