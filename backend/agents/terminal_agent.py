import subprocess
import os

FORBIDDEN_COMMANDS = [
    "format", "rmdir /s /q c:", "del /f /s /q c:", 
    "shutdown", "reg delete"
]

def run_command(command: str, cwd: str = None) -> dict:
    """Executes a shell command safely and returns the output."""
    clean_cmd = command.lower().strip()

    for forbidden in FORBIDDEN_COMMANDS:
        if forbidden in clean_cmd:
            return {
                "status": "error",
                "message": f"Execution blocked: Unsafe command detected ('{forbidden}')."
            }

    try:
        working_dir = cwd if cwd and os.path.exists(cwd) else os.getcwd()
        
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30
        )

        if process.returncode == 0:
            return {
                "status": "success",
                "output": process.stdout.strip() or "Command executed successfully.",
                "working_dir": working_dir
            }
        else:
            return {
                "status": "error",
                "output": process.stderr.strip() or "Command failed.",
                "working_dir": working_dir
            }

    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Command execution timed out (30s limit)."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to execute command: {str(e)}"}