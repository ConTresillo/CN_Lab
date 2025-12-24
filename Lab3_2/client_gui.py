import tkinter as tk
from tkinter import messagebox
import threading
from typing import Type, Optional


class ChatClientGUI:
    def __init__(self, client_class: Type) -> None:
        self.client_class = client_class
        self.client = None
        self.connected = False
        self.root = tk.Tk()
        self.root.title("Chat Room Client")

        # Setup GUI Components
        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Message (@user for private):").pack()
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack()

        self.connect_btn = tk.Button(self.root, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(pady=5)

        self.send_btn = tk.Button(self.root, text="Send", command=self.send_msg, state="disabled")
        self.send_btn.pack()

        self.output = tk.Text(self.root, height=15, width=60, state="disabled")
        self.output.pack()

        # Tags for Colors
        self.output.tag_config("user", foreground="blue")  # My msgs
        self.output.tag_config("system", foreground="red")  # Server/System
        self.output.tag_config("others", foreground="green")  # Other users
        self.output.tag_config("private", foreground="gray")  # Private msgs

    def write_log(self, msg: str, tag: str) -> None:
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n", tag)
        self.output.see("end")
        self.output.config(state="disabled")

    def listen_loop(self) -> None:
        while self.connected:
            msg = self.client.receive()
            if not msg: break

            tag = "others"
            if "(Private)" in msg:
                tag = "private"
            elif "[SYSTEM]" in msg:
                tag = "system"

            self.write_log(msg, tag)
        self.connected = False
        self.connect_btn.config(text="Connect")

    def toggle_connection(self) -> None:
        if not self.connected:
            u = self.username_entry.get()
            self.client = self.client_class(u)
            try:
                self.client.connect("127.0.0.1", 5000)
                self.connected = True
                self.connect_btn.config(text="Disconnect")
                self.send_btn.config(state="normal")
                threading.Thread(target=self.listen_loop, daemon=True).start()
                self.write_log("Connected!", "system")
            except:
                messagebox.showerror("Error", "Failed to connect")
        else:
            self.client.close()
            self.connected = False

    def send_msg(self) -> None:
        msg = self.entry.get()
        if msg:
            if msg.startswith("@"):
                self.write_log(f"To {msg.split()[0]}: {msg}", "private")
            else:
                self.write_log(f"Me: {msg}", "user")
            self.client.send(msg)
            self.entry.delete(0, "end")

    def start(self) -> None:
        self.root.mainloop()