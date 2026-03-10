from UI.TkinterMenu import TkinterUI

if __name__ == "__main__":
    try:
        TkinterUI()
    except KeyboardInterrupt:
        print("GUI closed by user")

