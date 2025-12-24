import tkinter as tk
from tkinter import messagebox
import threading
from typing import Type, Optional


class ClientGUI:
    """
    GUI handles the Color Logic.
    """

    def __init__(self, client_class: Type) -> None:
        self.client_class = client_class
        self.client = None
        self.connected = False

        # ---- Colors & Font ----
        BG, PANEL = "#FFF8E7", "#F3EED9"
        FG = "#4A3F2A"
        BTN = "#E6C97A"

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.configure(bg=BG)

        # Connection Inputs
        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", bg=PANEL).grid(row=0, column=0)
        self.user_entry = tk.Entry(frame)
        self.user_entry.grid(row=0, column=1)

        tk.Label(frame, text="Port:", bg=PANEL).grid(row=1, column=0)
        self.port_entry = tk.Entry(frame)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=1, column=1)

        self.connect_btn = tk.Button(frame, text="Connect", command=self.toggle_connection, bg=BTN)
        self.connect_btn.grid(row=2, columnspan=2, pady=5)

        # Output Area
        self.output = tk.Text(self.root, height=15, width=60, state="disabled", bg="#FFFDF6")
        self.output.pack(padx=10, pady=5)

        # ---- COLOR TAGS ----
        self.output.tag_config("me", foreground="#1E5EFF", font=("Segoe UI", 10, "bold"))
        self.output.tag_config("others", foreground="#008000", font=("Segoe UI", 10))
        self.output.tag_config("private", foreground="#808080", font=("Segoe UI", 10, "italic"))
        self.output.tag_config("system", foreground="#B00020", font=("Segoe UI", 10, "bold"))

        # Message Input
        self.msg_entry = tk.Entry(self.root, width=50, state="disabled")
        self.msg_entry.pack(pady=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_msg())

        self.send_btn = tk.Button(self.root, text="Send", command=self.send_msg, state="disabled", bg=BTN)
        self.send_btn.pack()

    def write_log(self, msg: str, tag: str) -> None:
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n", tag)
        self.output.see("end")
        self.output.config(state="disabled")

    def listen_loop(self) -> None:
        while self.connected:
            msg = self.client.receive()
            if msg is None: break

            # --- COLOR LOGIC FOR INCOMING ---
            if "(Private)" in msg:
                self.write_log(msg, "private")
            elif "[SYSTEM]" in msg:
                self.write_log(msg, "system")
            else:
                self.write_log(msg, "others")

        self.on_disconnect()

    def send_msg(self) -> None:
        msg = self.msg_entry.get().strip()
        if not msg: return

        self.msg_entry.delete(0, "end")

        if msg.startswith("@"):
            parts = msg.split(" ", 1)
            target = parts[0]
            self.write_log(f"(Private to {target}) : {parts[1] if len(parts) > 1 else ''}", "private")
        else:
            self.write_log(f"[Me]: {msg}", "me")

        try:
            self.client.send(msg)
        except:
            self.on_disconnect()

    def toggle_connection(self) -> None:
        if not self.connected:
            u = self.user_entry.get()
            try:
                p = int(self.port_entry.get())
                self.client = self.client_class(u)
                self.client.connect("127.0.0.1", p)

                self.connected = True
                self.connect_btn.config(text="Disconnect")
                self.msg_entry.config(state="normal")
                self.send_btn.config(state="normal")

                threading.Thread(target=self.listen_loop, daemon=True).start()
                self.write_log("[SYSTEM]: Connected", "system")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.client.close()
            self.on_disconnect()

    def on_disconnect(self):
        # --- FIX IS HERE ---
        if not self.connected:
            return  # Stop if already disconnected

        self.connected = False
        self.connect_btn.config(text="Connect")
        self.msg_entry.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.write_log("[SYSTEM]: Disconnected", "system")

    def start(self):
        self.root.mainloop()