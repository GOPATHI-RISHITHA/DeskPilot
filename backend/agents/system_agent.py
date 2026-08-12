import psutil
import pythoncom
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities

def get_system_stats() -> dict:
    """Returns CPU, Memory, and Battery metrics."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()

        battery_info = "No battery detected (Desktop)"
        if battery:
            battery_info = {
                "percentage": battery.percent,
                "power_plugged": battery.power_plugged
            }

        return {
            "status": "success",
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory.percent,
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "battery": battery_info
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve system stats: {str(e)}"}

def set_volume(level: int) -> dict:
    """Sets system volume (0 to 100)."""
    try:
        # Initialize COM thread for Windows audio controls
        pythoncom.CoInitialize()

        level = max(0, min(100, level))  # Clamp between 0 and 100

        # Modern pycaw syntax
        devices = AudioUtilities.GetSpeakers()
        if hasattr(devices, "EndpointVolume"):
            volume = devices.EndpointVolume
        else:
            # Fallback for low-level COM interface
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import IAudioEndpointVolume
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Set volume scalar from 0.0 to 1.0
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)

        pythoncom.CoUninitialize()
        return {"status": "success", "message": f"System volume set to {level}%"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to set volume: {str(e)}"}

def set_brightness(level: int) -> dict:
    """Sets monitor brightness (0 to 100)."""
    try:
        level = max(0, min(100, level))
        sbc.set_brightness(level)
        return {"status": "success", "message": f"Screen brightness set to {level}%"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to set brightness: {str(e)}"}