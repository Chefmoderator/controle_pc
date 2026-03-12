import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys

class LogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server Logs")
        self.root.geometry("900x500")
        self.root.configure(bg="#1e1e2f")

        self.text = ScrolledText(
            self.root,
            bg="#0f0f1f",
            fg="lime",
            font=("Consolas", 11),
            insertbackground="white"
        )
        self.text.pack(fill="both", expand=True)

        self.buffer = ""


        sys.stdout = self
        sys.stderr = self

        self.root.after(50, self.update_window)


    def isatty(self):
        return True

    def fileno(self):
        return 1


    def write(self, msg):
        self.buffer += msg

    def flush(self):
        pass

    def update_window(self):
        if self.buffer:
            self.text.insert(tk.END, self.buffer)
            self.text.see(tk.END)
            self.buffer = ""
        self.root.after(50, self.update_window)


    def write_from_loguru(self, message):
        self.write(message)

    def start(self):
        self.root.mainloop()