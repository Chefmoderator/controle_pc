from core.system_control import SystemMenu
from core.file_manager import FileMenu
from core.processes import ProcessesMenu
from core.mouse_keyboard import MouseKeyboardMenu

def menu():
    while True:
        print(
            "=== List of my process ===\n"
            "1. System control menu\n"
            "2. File manager\n"
            "3. Process manger\n"
            "4. Mouse-keyboard manager\n"
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
            case 3:
                ProcessesMenu.menu()
            case 4:
                MouseKeyboardMenu.menu()
            case 0:
                break
            case _:
                print("Unknown option")
                input("Press Enter...")

if __name__ == "__main__":
    menu()
