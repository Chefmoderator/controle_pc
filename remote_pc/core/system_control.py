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
        print("\n=== SYSTEM VERSION ===")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Full OS: {platform.platform()}")
        print()

    @staticmethod
    def get_user():
        print("\n=== USER INFO ===")
        print(f"PC name: {platform.node()}")
        print(f"User: {getpass.getuser()}")
        print()

    @staticmethod
    def get_computer_hardware():
        mem = psutil.virtual_memory()

        print("\n=== COMPUTER HARDWARE ===")
        print(f"CPU: {platform.processor()}")
        print(f"Machine: {platform.machine()}")

        print("\n=== RAM ===")
        print(f"Total RAM: {mem.total / 1024**3:.2f} GB")
        print(f"Used RAM: {mem.used / 1024**3:.2f} GB")
        print(f"Available RAM: {mem.available / 1024**3:.2f} GB")

        print("\n=== DISKS ===")
        for d in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(d.mountpoint)
                print(f"{d.device}: {usage.percent}% used")
            except PermissionError:
                pass
        print()

    @staticmethod
    def get_temperature():
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                print("Temperature sensors not available.\n")
                return

            print("\n=== TEMPERATURES ===")
            for name, entries in temps.items():
                print(f"{name}:")
                for sensor in entries:
                    label = sensor.label or "Sensor"
                    print(f"  {label}: {sensor.current}°C")
            print()

        except Exception:
            print("Temperature sensors not available.\n")

    @staticmethod
    def get_uptime():
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        diff = datetime.datetime.now() - boot

        print("\n=== UPTIME ===")
        print(f"Boot time: {boot}")
        print(f"Uptime: {diff.days} days, {diff.seconds // 3600} hours\n")

    @staticmethod
    def get_battery():
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                print("Battery not detected\n")
                return

            print("\n=== BATTERY ===")
            print(f"Level: {battery.percent}%")
            print(f"Plugged in: {'Yes' if battery.power_plugged else 'No'}")

            if battery.secsleft > 0:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                print(f"Time left: {hours}h {minutes}m\n")
            else:
                print("Time left: unlimited\n")

        except Exception:
            print("Battery information not available.\n")


class PowerManagement:

    @staticmethod
    def shutdown():
        print("Power off PC")
        os.system("shutdown /s /t 0")

    @staticmethod
    def restart():
        print("Restart PC")
        os.system("shutdown /r /t 0")

    @staticmethod
    def sleep():
        print("PC sleep")
        os.system("powercfg -h on")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    @staticmethod
    def hibernate():
        print("Hibernate PC")
        os.system("shutdown /h")


class LaunchProgram:

    @staticmethod
    def find_file(start_path, filename):
        for root, dirs, files in os.walk(start_path):
            if filename in files:
                return os.path.join(root, filename)
        return None

    @staticmethod
    def launch_program():
        exe_name = input("Enter your program name or full path > ").strip()

        if not exe_name.lower().endswith(".exe") and "\\" not in exe_name:
            exe_name += ".exe"

        if "\\" in exe_name and os.path.isfile(exe_name):
            path = exe_name
        else:
            print(f"Searching for: {exe_name}")
            path = LaunchProgram.find_file("C:\\", exe_name)

        if path:
            try:
                print(f"Opening: {path}")
                subprocess.Popen(path)
            except Exception as e:
                print(f"Cannot open program: {e}")
        else:
            print("Program not found.")


class RemoteVolume:
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    @staticmethod
    def mute():
        RemoteVolume.volume.SetMute(True, None)
        print("Sound muted")

    @staticmethod
    def unmute():
        RemoteVolume.volume.SetMute(False, None)
        print("Sound unmuted")

    @staticmethod
    def set_volume():
        try:
            new_volume = int(input("Enter new volume (0–100) > "))
            if not 0 <= new_volume <= 100:
                print("Invalid range")
                return
            RemoteVolume.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
            print(f"Volume set to {new_volume}%")
        except ValueError:
            print("Please enter a number")

    @staticmethod
    def get_volume():
        current_volume = RemoteVolume.volume.GetMasterVolumeLevelScalar()
        print(f"Current volume: {int(current_volume * 100)}%")


class ScreenBrightnessControl:
    @staticmethod
    def get_brightness():
        try:
            b = sbc.get_brightness()
            print(f"Screen brightness: {b[0]}%")
        except Exception as e:
            print(f"Cannot get brightness: {e}")

    @staticmethod
    def set_brightness():
        try:
            new_brightness = int(input("Enter new screen brightness (0–100) > "))
            if not 0 <= new_brightness <= 100:
                print("Invalid range")
                return
            sbc.set_brightness(new_brightness)
            print(f"Brightness set to {new_brightness}%")
        except Exception as e:
            print(f"Cannot set brightness: {e}")


class SystemMenu:

    @staticmethod
    def menu():
        while True:
            print("\n"
                    "=== SYSTEM CONTROL MENU ===\n"
                    "1. Info manager\n"
                    "2. Power management\n"
                    "3. Launch program\n"
                    "4. Remote volume\n"
                    "5. Screen brightness control"
            )
            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: SystemMenu.info()
                case 2: SystemMenu.power()
                case 3: SystemMenu.launch()
                case 4: SystemMenu.volume()
                case 5: SystemMenu.brightness()
                case 0: break
                case _: print("Unknown option")

    @staticmethod
    def info():
        while True:
            print(
                "\n=== INFO MENU ===\n"
                "1. System version\n"
                "2. Computer hardware\n"
                "3. Uptime\n"
                "4. Temperature\n"
                "5. Battery\n"
                "6. Users\n"
                "0. Exit\n"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: InfoManager.get_system_version()
                case 2: InfoManager.get_computer_hardware()
                case 3: InfoManager.get_uptime()
                case 4: InfoManager.get_temperature()
                case 5: InfoManager.get_battery()
                case 6: InfoManager.get_user()
                case 0: break
                case _: print("Unknown option")

            input("Press Enter to continue...")

    @staticmethod
    def power():
        while True:
            print(
                "\n=== POWER MANAGEMENT MENU ===\n"
                "1. Shutdown\n"
                "2. Restart\n"
                "3. Sleep\n"
                "4. Hibernate\n"
                "0. Exit\n"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: PowerManagement.shutdown()
                case 2: PowerManagement.restart()
                case 3: PowerManagement.sleep()
                case 4: PowerManagement.hibernate()
                case 0: break
                case _: print("Unknown option")

            input("Press Enter to continue...")

    @staticmethod
    def launch():
        while True:
            print(
                "\n=== LAUNCH PROGRAM MENU ===\n"
                "1. Launch program\n"
                "0. Exit"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: LaunchProgram.launch_program()
                case 0: break
                case _: print("Unknown option")

            input("Press Enter to continue...")

    @staticmethod
    def volume():
        while True:
            print(
                "\n=== REMOTE VOLUME MENU ===\n"
                "1. Mute\n"
                "2. Unmute\n"
                "3. Set volume\n"
                "4. Get Volume\n"
                "0. Exit\n"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: RemoteVolume.mute()
                case 2: RemoteVolume.unmute()
                case 3: RemoteVolume.set_volume()
                case 4: RemoteVolume.get_volume()
                case 0: break
                case _: print("Unknown option")

            input("Press Enter to continue...")

    @staticmethod
    def brightness():
        while True:
            print(
                "\n=== SCREEN BRIGHTNESS CONTROL MENU ===\n"
                "1. Get brightness\n"
                "2. Set brightness\n"
                "0. Exit\n"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Enter a number.")
                continue

            match n:
                case 1: ScreenBrightnessControl.get_brightness()
                case 2: ScreenBrightnessControl.set_brightness()
                case 0: break
                case _: print("Unknown option")

            input("Press Enter to continue...")
