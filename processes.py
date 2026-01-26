import subprocess
import psutil
import datetime

class ProcessManger:

    @staticmethod
    def list_processes():
        print(f"{'Username':<20}{'PID':<10}{'Name':<30}{'Memory(MB)':<15}")
        print("-" * 75)

        for proc in psutil.process_iter(['name', 'pid', 'username', 'memory_info']):
            try:
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                print(f"{proc.info['username']:<20}{proc.info['pid']:<10}{proc.info['name']:<30}{mem:<15.2f}")
            except psutil.NoSuchProcess:
                pass

    @staticmethod
    def search_process():
        name = input("Enter process name > ").strip().lower()
        found = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name and name in proc_name.lower():
                    found.append(proc.info)
            except psutil.NoSuchProcess:
                pass

        if not found:
            print("Process not found.")
        else:
            print("Found processes:")
            for p in found:
                print(f"PID: {p['pid']}  Name: {p['name']}")

    @staticmethod
    def kill_process():
        pid = input("Enter process PID > ").strip()
        try:
            pid = int(pid)
            proc = psutil.Process(pid)
            proc.terminate()
            print(f"Process {pid} terminated.")
        except psutil.NoSuchProcess:
            print("Process not found.")
        except ValueError:
            print("PID must be a number.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def start_process():
        path = input("Enter process path >")
        try:
            subprocess.Popen(path)
            print("Process started.")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def restart_process():
        pid = input("Enter process PID > ").strip()
        try:
            pid = int(pid)
            proc = psutil.Process(pid)
            exe = proc.exe()

            proc.terminate()
            proc.wait()

            subprocess.Popen(exe)
            print(f"Process {pid} restarted.")
        except psutil.NoSuchProcess:
            print("Process not found.")
        except psutil.AccessDenied:
            print("Access denied. Run script as admin.")
        except ValueError:
            print("PID must be a number.")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def process_info():
        pid = int(input("Enter process PID").strip())
        try:
            proc = psutil.Process(pid)
            proc.cpu_percent(interval=None)

            print(f"\n=== Process info for PID {pid} ===")
            print(f"1. Name:         {proc.name()}")
            print(f"2. Executable:   {proc.exe()}")
            print(f"3. Status:       {proc.status()}")
            print(f"4. Started:      {datetime.datetime.fromtimestamp(proc.create_time())}")
            print(f"5. CPU %:        {proc.cpu_percent(interval=0.2)}")
            print(f"6. Memory MB:    {proc.memory_info().rss / (1024 * 1024):.2f}")
            print(f"7. Parent PID:   {proc.ppid()}")

        except psutil.NoSuchProcess:
            print("Error: Process does not exist.")
        except psutil.AccessDenied:
            print("Error: Access denied. Try running as administrator.")
        except ValueError:
            print("Error: PID must be a number.")
        except Exception as e:
            print("Unexpected error:", e)
        


class ProcessesMenu:

    @staticmethod
    def menu():
        while True:
            print(
                "=== List process manager ===\n"
                "1. List processes\n"
                "2. Search process \n"
                "3. Kill process\n"
                "4. Start process\n"
                "5. Restart process\n"
                "6. Process info\n"
                "0. Exit\n"
            )

            try:
                n = int(input("Enter choice > "))
            except ValueError:
                print("Please enter a number")
                input("Press Enter...")
                continue

            match n:
                case 1:
                    ProcessManger.list_processes()
                case 2:
                    ProcessManger.search_process()
                case 3:
                    ProcessManger.kill_process()
                case 4:
                    ProcessManger.start_process()
                case 5:
                    ProcessManger.restart_process()
                case 6:
                    ProcessManger.process_info()
                case 0:
                    break
                case _:
                    print("Unknown option")
                    input("Press Enter...")