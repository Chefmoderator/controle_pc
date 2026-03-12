import os
import tkinter as tk
from tkinter import messagebox
from Server import Server
import re
import threading
from sertificate import createCertificate

class TkinterUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server Config")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2f")

        tk.Label(
            self.root,
            text="Server Configuration",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(20, 15))


        self.ip_entry = self.create_input("IP")
        self.port_entry = self.create_input("Port")


        self.start_button = tk.Button(
            self.root,
            text="START SERVER",
            font=("Helvetica", 12, "bold"),
            bg="#4caf50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief="flat",
            command=self.start_server
        )
        self.start_button.pack(pady=20, ipadx=10, ipady=5)
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg="#45a049"))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg="#4caf50"))
        self.root.mainloop()


    def create_input(self, placeholder):
        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(pady=8)
        entry = tk.Entry(frame, font=("Helvetica", 12), width=30, bd=0, fg="white", bg="#2e2e3f",
                         insertbackground="white")
        entry.pack(padx=5, ipady=5)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, ent=entry, ph=placeholder: self._clear_placeholder(e, ent, ph))
        entry.bind("<FocusOut>", lambda e, ent=entry, ph=placeholder: self._add_placeholder(e, ent, ph))
        return entry

    def _clear_placeholder(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="white")

    def _add_placeholder(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def start_server(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        ip_pattern = r"^(https?://)?([a-zA-Z0-9\-\.]+)(:\d+)?$"
        if not re.match(ip_pattern, ip):
            messagebox.showerror("Error", "Please enter a valid IP or URL")
            return

        if not port.isdigit():
            messagebox.showerror("Error", "Port must be a number")
            return

        port = int(port)
        full_url = f"{ip}:{port}"

        if not (os.path.exists("cert.pem") and os.path.exists("key.pem")):
            createCertificate(ip)

        messagebox.showinfo("Server Start", f"Server started at:\n{full_url}")

        threading.Thread(target=lambda: Server(ip, port)).start()
        self.root.destroy()