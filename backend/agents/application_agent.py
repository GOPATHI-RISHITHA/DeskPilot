import os
import subprocess
import psutil

APP_MAP = {
    # Browsers
    "edge": "msedge",
    "msedge": "msedge",
    "microsoft-edge": "msedge",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    
    # Editors & IDEs
    "vscode": "code",
    "code": "code",
    "notepad": "notepad",
    
    # Communication & Media
    "spotify": "spotify:",
    "whatsapp": "whatsapp:",
    "discord": os.path.expandvars(r"%LOCALAPPDATA%\Discord\Update.exe --processStart Discord.exe"),
    
    # Windows Utilities
    "paint": "mspaint",
    "mspaint": "mspaint",
    "calculator": "calc",
    "calc": "calc",
    "cmd": "cmd",
    "powershell": "powershell",
    "explorer": "explorer",
    "settings": "ms-settings:",
    "taskmanager": "taskmgr",
    "controlpanel": "control"
}

PROCESS_MAP = {
    "vscode": "Code.exe",
    "code": "Code.exe",
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "calculator": "CalculatorApp.exe",
    "edge": "msedge.exe",
    "msedge": "msedge.exe",
    "spotify": "Spotify.exe"
}

def open_app(app_name: str) -> dict:
    """Launches an application reliably on Windows."""
    clean_name = app_name.lower().strip()
    target = APP_MAP.get(clean_name, clean_name)

    try:
        # Method 1: Protocol URIs (e.g., spotify:, ms-settings:)
        if target.endswith(":"):
            os.system(f"start {target}")
            return {"status": "success", "message": f"Opened {app_name} via protocol."}

        # Method 2: Standard executables / system apps via shell execution
        subprocess.Popen(f"start {target}", shell=True)
        return {"status": "success", "message": f"Opened {app_name} successfully."}

    except Exception as e:
        try:
            # Fallback Method 3: Direct os.startfile or shell fallback
            os.startfile(target)
            return {"status": "success", "message": f"Launched {app_name} via startfile."}
        except Exception as err:
            return {"status": "error", "message": f"Failed to open {app_name}: {str(err)}"}


def close_app(app_name: str) -> dict:
    """Terminates running instances of an application."""
    clean_name = app_name.lower().strip()
    process_exe = PROCESS_MAP.get(clean_name, f"{clean_name}.exe")

    closed = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == process_exe.lower():
                proc.kill()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if closed:
        return {"status": "success", "message": f"Closed {app_name} successfully."}
    return {"status": "warning", "message": f"No running process found for {app_name}."}


def list_running_apps() -> dict:
    """Lists running process count."""
    running = []
    for proc in psutil.process_iter(['name']):
        try:
            p_name = proc.info['name']
            if p_name and p_name not in running:
                running.append(p_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {"status": "success", "running_processes_count": len(running)}