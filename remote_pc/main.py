from core.system_control import SystemMenu
from core.file_manager import FileMenu

def menu():
    while True:
        print(
            "=== List of my process ===\n"
            "1. System control menu\n"
            "2. File manager\n"
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
                SystemMenu.menu()
            case 2:
                FileMenu.menu()
            case 0:
                break
            case _:
                print("Unknown option")
                input("Press Enter...")

if __name__ == "__main__":
    menu()
