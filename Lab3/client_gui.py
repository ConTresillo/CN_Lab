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

        # ---- Colors ----
        BG = "#FFF8E7"
        PANEL = "#F3EED9"
        FG = "#4A3F2A"
        ENTRY_BG = "#FFFDF6"
        BTN = "#E6C97A"
        BTN_ACTIVE = "#D9B85C"

        self.root: tk.Tk = tk.Tk()
        self.root.title("Echo Client")
        self.root.configure(bg=BG)

        # ---- Connection frame ----
        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=8)

        tk.Label(frame, text="Username", bg=PANEL, fg=FG).grid(row=0, column=0, padx=5, pady=4)
        self.username_entry = tk.Entry(
            frame, bg=ENTRY_BG, fg=FG, insertbackground=FG
        )
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Server IP", bg=PANEL, fg=FG).grid(row=1, column=0, padx=5, pady=4)
        self.ip_entry = tk.Entry(
            frame, bg=ENTRY_BG, fg=FG, insertbackground=FG
        )
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=1, column=1)

        tk.Label(frame, text="Port", bg=PANEL, fg=FG).grid(row=2, column=0, padx=5, pady=4)
        self.port_entry = tk.Entry(
            frame, bg=ENTRY_BG, fg=FG, insertbackground=FG
        )
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=2, column=1)

        self.connect_btn = tk.Button(
            frame,
            text="Connect",
            command=self.toggle_connection,
            bg=BTN,
            fg=FG,
            activebackground=BTN_ACTIVE,
            relief="flat"
        )
        self.connect_btn.grid(row=3, column=0, columnspan=2, pady=8)

        # ---- Messaging ----
        tk.Label(self.root, text="Message", bg=BG, fg=FG).pack(pady=(5, 0))

        self.entry = tk.Entry(
            self.root,
            width=50,
            state="disabled",
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG
        )
        self.entry.pack()

        self.send_btn = tk.Button(
            self.root,
            text="Send",
            state="disabled",
            command=self.send_msg,
            bg=BTN,
            fg=FG,
            activebackground=BTN_ACTIVE,
            relief="flat"
        )
        self.send_btn.pack(pady=4)

        self.output = tk.Text(
            self.root,
            height=15,
            width=60,
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG,
            relief="flat"
        )
        # ---- Text styling tags ----
        self.output.tag_configure(
            "user",
            foreground="#1E5EFF"  # blue
        )

        self.output.tag_configure(
            "system",
            foreground="#B00020",  # red
            font=("Segoe UI", 10, "bold")
        )

        self.output.pack(padx=10, pady=6)

    def write_log(self, msg: str, tag: str = "system") -> None:
        self.output.insert("end", msg + "\n", tag)
        self.output.see("end")

    # ---------------- LISTENER ----------------

    def listen_loop(self) -> None:
        while self.connected and self.client:
            msg = self.client.receive()
            if msg is None:
                break
            self.write_log(f"[SERVER] : {msg}", "system")

        self.on_disconnect()

    def on_disconnect(self) -> None:
        if not self.connected:
            return

        self.connected = False
        self.entry.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.connect_btn.config(text="Connect")
        self.write_log("[SYSTEM] : Disconnected", "system")

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
            self.write_log(f"[SYSTEM] : Connected to {ip}:{port}", "system")

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
        self.write_log(f"[{self.client.username}] : {msg}", "user")

        try:
            self.client.send(msg)
        except Exception:
            self.on_disconnect()

    def start(self) -> None:
        self.root.mainloop()
