import subprocess
import psutil
import datetime

class ProcessManager:

    @staticmethod
    def list_processes():
        result = []
        for proc in psutil.process_iter(['name', 'pid', 'username', 'memory_info']):
            try:
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                result.append({
                    "username": proc.info['username'],
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "memory_mb": round(mem, 2)
                })
            except psutil.NoSuchProcess:
                pass
        return result

    @staticmethod
    def search_process(name: str):
        name = name.lower()
        found = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name and name in proc_name.lower():
                    found.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name']
                    })
            except psutil.NoSuchProcess:
                pass

        return found

    @staticmethod
    def kill_process(pid: int):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return {"status": "terminated", "pid": pid}
        except psutil.NoSuchProcess:
            return {"error": "process_not_found", "pid": pid}
        except psutil.AccessDenied:
            return {"error": "access_denied"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def start_process(path: str):
        try:
            subprocess.Popen(path)
            return {"status": "started", "path": path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def restart_process(pid: int):
        try:
            proc = psutil.Process(pid)
            exe_path = proc.exe()

            proc.terminate()
            proc.wait()

            subprocess.Popen(exe_path)

            return {
                "status": "restarted",
                "pid": pid,
                "exe": exe_path
            }

        except psutil.NoSuchProcess:
            return {"error": "process_not_found"}
        except psutil.AccessDenied:
            return {"error": "access_denied"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def process_info(pid: int):
        try:
            proc = psutil.Process(pid)

            return {
                "pid": pid,
                "name": proc.name(),
                "exe": proc.exe(),
                "status": proc.status(),
                "start_time": str(datetime.datetime.fromtimestamp(proc.create_time())),
                "cpu_percent": proc.cpu_percent(interval=0.2),
                "memory_mb": round(proc.memory_info().rss / (1024 * 1024), 2),
                "parent_pid": proc.ppid()
            }

        except psutil.NoSuchProcess:
            return {"error": "process_not_found"}
        except psutil.AccessDenied:
            return {"error": "access_denied"}
        except Exception as e:
            return {"error": str(e)}
