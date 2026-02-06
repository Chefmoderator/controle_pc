import os
import subprocess
import platform
import getpass
import psutil
import datetime
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

class InfoManager:

    @staticmethod
    def get_system_version():
        return {
            "os": f"{platform.system()} {platform.release()}",
            "full_os": platform.platform()
        }

    @staticmethod
    def get_user():
        return {
            "pc_name":platform.node(),
            "user": getpass.getuser()
        }

    @staticmethod
    def get_computer_hardware():
        mem = psutil.virtual_memory()

        disks = []
        for d in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(d.mountpoint)
                disks.append({
                    "device": d.device,
                    "mountpoint": d.mountpoint,
                    "used_percent": usage.percent
                })
            except PermissionError:
                pass

        return {
            "cpu": platform.processor(),
            "machine": platform.machine(),

            "ram": {
                "total_gb": round(mem.total / 1024 ** 3, 2),
                "used_gb": round(mem.used / 1024 ** 3, 2),
                "available_gb": round(mem.available / 1024 ** 3, 2),
            },

            "disks": disks
        }

    @staticmethod
    def get_temperature():
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return {"error": "Temperature sensors not available"}
            result = {}

            for name, entries in temps.items():
                result[name] = []
                for sensor in entries:
                    label = sensor.label or "Sensor"
                    result[name].append({
                        "label": label,
                        "temperature_c": sensor.current
                    })
            return result
        except Exception:
            return {"error": "Temperature sensors not available"}

    @staticmethod
    def get_uptime():
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        diff = datetime.datetime.now() - boot

        print("\n=== UPTIME ===")
        print(f"Boot time: {boot}")
        print(f"Uptime: {diff.days} days, {diff.seconds // 3600} hours\n")
        return {
            "boot_time":boot,
            "uptime": f"{diff.days} days, {diff.seconds // 3600} hours"
        }

    @staticmethod
    def get_battery():
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return {
                    "battery_detected": False
                }
            result = {
                "battery_detected": True,
                "level_percent": battery.percent,
                "plugged_in": battery.power_plugged,
            }
            if battery.secsleft > 0:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                result["time_left"] = f"{hours}h {minutes}m"
            else:
                result["time_left"] = "unlimited"
            return result
        except Exception:
            return {
                "battery_detected": False,
                "error": "Battery information not available"
            }

    @staticmethod
    def info_manager_json():
        result = {}

        methods_to_call = [
            "get_system_version",
            "get_user",
            "get_computer_hardware",
            "get_temperature",
            "get_uptime",
            "get_battery"
        ]

        for method_name in methods_to_call:
            method = getattr(InfoManager, method_name)
            result[method_name] = method()

        return result


class PowerManagement:

    @staticmethod
    def shutdown():
        os.system("shutdown /s /t 0")
        return {"power_status": "Power off"}

    @staticmethod
    def restart():
        os.system("shutdown /r /t 0")
        return {"power_status": "Restart"}

    @staticmethod
    def sleep():
        os.system("powercfg -h on")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return {"power_status": "Sleep"}

    @staticmethod
    def hibernate():
        os.system("shutdown /h")
        return {"power_status": "Hibernate"}


class LaunchProgram:

    @staticmethod
    def find_file(start_path, filename):

        for root, dirs, files in os.walk(start_path):
            if filename in files:
                return os.path.join(root, filename)
        return None

    @staticmethod
    def launch_program(exe_name: str):
        exe_name = exe_name.strip()
        if not exe_name.lower().endswith(".exe") and "\\" not in exe_name:
            exe_name += ".exe"

        if "\\" in exe_name and os.path.isfile(exe_name):
            path = exe_name
        else:
            path = LaunchProgram.find_file("C:\\", exe_name)

        if path:
            try:
                subprocess.Popen(path)
                return {"status": "success", "path": path, "message": f"{exe_name} launched"}
            except Exception as e:
                return {"status": "error", "path": path, "message": str(e)}
        else:
            return {"status": "error", "message": "Program not found"}


class RemoteVolume:
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    @staticmethod
    def mute():
        RemoteVolume.volume.SetMute(True, None)
        return {"volume_status": "muted"}

    @staticmethod
    def unmute():
        RemoteVolume.volume.SetMute(False, None)
        return {"volume_status": "unmuted"}

    @staticmethod
    def set_volume(new_volume: int):
        if not 0 <= new_volume <= 100:
            return {"error": "Volume must be between 0 and 100"}
        RemoteVolume.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
        return {"volume_status": f"set to {new_volume}%"}

    @staticmethod
    def get_volume():
        current_volume = RemoteVolume.volume.GetMasterVolumeLevelScalar()
        return {"current_volume": int(current_volume * 100)}


class ScreenBrightnessControl:
    @staticmethod
    def get_brightness():
        try:
            brightness_list = sbc.get_brightness()
            brightness = brightness_list[0] if brightness_list else None
            return {"brightness": brightness}
        except Exception as e:
            return {"error": f"Cannot get brightness: {e}"}

    @staticmethod
    def set_brightness(new_brightness: int):
        try:
            if not 0 <= new_brightness <= 100:
                return {"error": "Brightness must be between 0 and 100"}
            sbc.set_brightness(new_brightness)
            return {"brightness_status": f"set to {new_brightness}%"}
        except Exception as e:
            return {"error": f"Cannot set brightness: {e}"}

