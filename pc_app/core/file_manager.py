import os
import shutil
import zipfile


class FileManager:

    @staticmethod
    def searching_file(filename: str):
        filename = filename.strip()
        for root, dirs, files in os.walk("C:\\"):
            if filename in files:
                path = os.path.join(root, filename)
                return {"found": True, "path": path}
        return {"found": False, "error": "File not found"}

    @staticmethod
    def inspection_of_folders(path: str):
        path = path.strip()
        try:
            items = os.listdir(path)
            return {"path": path, "items": items}
        except FileNotFoundError:
            return {"error": "Path not found"}
        except PermissionError:
            return {"error": "No permission to access this folder"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def create_folder(path: str):
        try:
            os.makedirs(path, exist_ok=True)
            return {"created": True, "path": path}
        except Exception as e:
            return {"created": False, "error": str(e)}

    @staticmethod
    def create_file(path: str, content: str = ""):
        try:
            with open(path, "w") as f:
                f.write(content)
            return {"created": True, "path": path}
        except Exception as e:
            return {"created": False, "error": str(e)}

    @staticmethod
    def delete_item(path: str):
        try:
            if os.path.isfile(path):
                os.remove(path)
                return {"deleted": True, "type": "file"}
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return {"deleted": True, "type": "folder"}
            else:
                return {"deleted": False, "error": "File or folder does not exist"}
        except Exception as e:
            return {"deleted": False, "error": str(e)}

    @staticmethod
    def move_item(src: str, dst: str):
        try:
            shutil.move(src, dst)
            return {"moved": True, "from": src, "to": dst}
        except Exception as e:
            return {"moved": False, "error": str(e)}

    @staticmethod
    def create_zip(source: str, zip_path: str):
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source):
                    zipf.write(source, os.path.basename(source))
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, source)
                            zipf.write(full_path, rel_path)

            return {"archived": True, "zip_path": zip_path}
        except Exception as e:
            return {"archived": False, "error": str(e)}

    @staticmethod
    def read_file(path: str):
        try:
            with open(path, "r") as f:
                return {"path": path, "content": f.read()}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def edit_file(path: str, new_text: str):
        try:
            with open(path, "w") as f:
                f.write(new_text)
            return {"updated": True, "path": path}
        except Exception as e:
            return {"updated": False, "error": str(e)}