import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys


class LogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server Logs")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e2f")

        self.text = ScrolledText(
            self.root, bg="#0f0f1f", fg="lime",
            font=("Consolas", 11), insertbackground="white"
        )
        self.text.pack(fill="both", expand=True)
        sys.stdout = self
        sys.stderr = self
        self.buffer = ""
        self.root.after(100, self.check_updates)

    def isatty(self):
        return False

    def fileno(self):
        return 1

    def write(self, msg):
        self.buffer += msg

    def flush(self):
        pass

    def check_updates(self):
        if self.buffer:
            self.text.insert(tk.END, self.buffer)
            self.text.see(tk.END)
            self.buffer = ""
        self.root.after(50, self.check_updates)

    def start(self):
        self.root.mainloop()