import os
import shutil
import zipfile


class FileManager:

        @staticmethod
        def searching_file():
            filename = input("Enter your file name > ").strip()

            path = None
            for root, dirs, files in os.walk("C:\\"):
                if filename in files:
                    path = os.path.join(root, filename)
                    break

            if path:
                print(f"Your file is found at: {path}")
            else:
                print("File not found.")

        @staticmethod
        def inspection_of_folders():
            path = input("Enter path > ").strip()

            try:
                items = os.listdir(path)
                print("\nItems in folder:")
                for i in items:
                    print(" -", i)
            except FileNotFoundError:
                print("Path not found.")
            except PermissionError:
                print("No permission to access this folder.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def create_folder():
            path = input("Enter new folder path > ").strip()
            try:
                os.makedirs(path, exist_ok=True)
                print("Folder created.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def create_file():
            path = input("Enter new file path > ").strip()
            try:
                with open(path, "w") as f:
                    content = input("Enter content (leave empty for blank file): ")
                    f.write(content)
                print("File created.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def delete_item():
            path = input("Enter file/folder path to delete > ").strip()
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print("File deleted.")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print("Folder deleted.")
                else:
                    print("File or folder does not exist.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def move_item():
            src = input("Enter source path > ").strip()
            dst = input("Enter destination path > ").strip()

            try:
                shutil.move(src, dst)
                print("Moved successfully.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def create_zip():
            source = input("Enter file/folder to archive > ").strip()
            zip_path = input("Enter output zip path > ").strip()

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

                print("Zip created.")
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def read_file():
            path = input("Enter file path > ").strip()
            try:
                with open(path, "r") as f:
                    print("\nFile content:\n")
                    print(f.read())
            except Exception as e:
                print("Error:", e)

        @staticmethod
        def edit_file():
            path = input("Enter file path > ").strip()

            try:
                print("Current content:\n")
                with open(path, "r") as f:
                    print(f.read())

                new_text = input("\nEnter new content (rewrite entire file):\n")
                with open(path, "w") as f:
                    f.write(new_text)

                print("File updated.")
            except Exception as e:
                print("Error:", e)


class FileMenu:

    @staticmethod
    def menu():
        while True:
            print("\n"
                  "=== FILE MANAGER MENU ===\n"
                  "1. Searching file\n"
                  "2. Inspection of folders\n"
                  "3. Create folder\n"
                  "4. Create file\n"
                  "5. Delete item\n"
                  "6. Move item\n"
                  "7. Create zip\n"
                  "8. Read file\n"
                  "9. Edit file\n"
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
                    FileManager.searching_file()
                case 2:
                    FileManager.inspection_of_folders()
                case 3:
                    FileManager.create_folder()
                case 4:
                    FileManager.create_file()
                case 5:
                    FileManager.delete_item()
                case 6:
                    FileManager.move_item()
                case 7:
                    FileManager.create_zip()
                case 8:
                    FileManager.read_file()
                case 9:
                    FileManager.edit_file()
                case 0:
                    break
                case _:
                    print("Unknown option")

            input("Press Enter...")

