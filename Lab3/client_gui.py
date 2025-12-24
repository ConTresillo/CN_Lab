import tkinter as tk
from tkinter import messagebox
import threading
from typing import Type, Optional


class ClientGUI:
    """
    Tkinter GUI for Echo Client.
    Handles UI only. No socket logic here.
    """

    def __init__(self, client_class: Type) -> None:
        self.client_class: Type = client_class
        self.client: Optional[object] = None
        self.connected: bool = False

        self.root: tk.Tk = tk.Tk()
        self.root.title("Echo Client")

        # ---- Connection frame ----
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Server IP").grid(row=1, column=0)
        self.ip_entry = tk.Entry(frame)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=1, column=1)

        tk.Label(frame, text="Port").grid(row=2, column=0)
        self.port_entry = tk.Entry(frame)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=2, column=1)

        self.connect_btn = tk.Button(frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # ---- Messaging ----
        tk.Label(self.root, text="Message").pack()
        self.entry = tk.Entry(self.root, width=50, state="disabled")
        self.entry.pack()

        self.send_btn = tk.Button(self.root, text="Send", state="disabled", command=self.send_msg)
        self.send_btn.pack()

        self.output = tk.Text(self.root, height=15, width=60)
        self.output.pack()

    def write_log(self, msg: str) -> None:
        self.output.insert("end", msg + "\n")
        self.output.see("end")

    # ---------------- LISTENER ----------------

    def listen_loop(self) -> None:
        """
        Background listener thread.
        ONLY calls client.receive()
        """
        while self.connected and self.client:
            msg = self.client.receive()
            if msg is None:
                break
            self.write_log(f"[server]: {msg}")

        self.on_disconnect()

    def on_disconnect(self) -> None:
        """
        Centralized disconnect handling.
        """
        if not self.connected:
            return

        self.connected = False
        self.entry.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.connect_btn.config(text="Connect")
        self.write_log("[server]: Disconnected")

    # ---------------- CONNECTION ----------------

    def toggle_connection(self) -> None:
        if not self.connected:
            username = self.username_entry.get().strip()
            ip = self.ip_entry.get().strip()

            try:
                port = int(self.port_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Port must be a number")
                return

            if not username:
                messagebox.showerror("Error", "Username required")
                return

            self.client = self.client_class(username)

            try:
                self.client.connect(ip, port)
            except Exception as e:
                messagebox.showerror("Error", f"Connection failed: {e}")
                return

            self.connected = True
            self.connect_btn.config(text="Disconnect")
            self.entry.config(state="normal")
            self.send_btn.config(state="normal")

            threading.Thread(target=self.listen_loop, daemon=True).start()
            self.write_log(f"[server]: Connected to {ip}:{port}")

        else:
            if self.client:
                self.client.close()
            self.on_disconnect()

    # ---------------- SEND ----------------

    def send_msg(self) -> None:
        if not self.connected or not self.client:
            return

        msg = self.entry.get().strip()
        if not msg:
            return

        self.entry.delete(0, "end")
        self.write_log(f"[{self.client.username}]: {msg}")

        try:
            self.client.send(msg)
        except Exception:
            self.on_disconnect()

    def start(self) -> None:
        self.root.mainloop()
