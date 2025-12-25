import tkinter as tk
from tkinter import messagebox
import threading


class ClientGUI:
    """
    GUI handles presentation + user interaction only.
    """

    def __init__(self, client) -> None:
        self.client = client
        self.connected = False

        # ---- Colors ----
        BG, PANEL = "#FFF8E7", "#F3EED9"
        FG = "#4A3F2A"
        BTN = "#E6C97A"

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.configure(bg=BG)

        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=10)

        # ---- Inputs ----
        tk.Label(frame, text="Username:", bg=PANEL).grid(row=0, column=0)
        self.user_entry = tk.Entry(frame)
        self.user_entry.grid(row=0, column=1)

        tk.Label(frame, text="Server IP:", bg=PANEL).grid(row=1, column=0)
        self.host_entry = tk.Entry(frame)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.grid(row=1, column=1)

        tk.Label(frame, text="Port:", bg=PANEL).grid(row=2, column=0)
        self.port_entry = tk.Entry(frame)
        self.port_entry.insert(0, "55555")
        self.port_entry.grid(row=2, column=1)

        self.connect_btn = tk.Button(
            frame, text="Connect", command=self.toggle_connection, bg=BTN
        )
        self.connect_btn.grid(row=3, columnspan=2, pady=5)

        # ---- Output ----
        self.output = tk.Text(
            self.root, height=15, width=60, state="disabled", bg="#FFFDF6"
        )
        self.output.pack(padx=10, pady=5)

        # ---- COLOR TAGS ----
        self.output.tag_config(
            "me", foreground="#1E5EFF", font=("Segoe UI", 10, "bold")
        )
        self.output.tag_config(
            "others", foreground="#008000", font=("Segoe UI", 10)
        )
        self.output.tag_config(
            "private", foreground="#808080", font=("Segoe UI", 10, "italic")
        )
        self.output.tag_config(
            "system", foreground="#B00020", font=("Segoe UI", 10, "bold")
        )

        # ---- Message input ----
        self.msg_entry = tk.Entry(self.root, width=50, state="disabled")
        self.msg_entry.pack(pady=5)
        self.msg_entry.bind("<Return>", lambda _: self.send_msg())

        self.send_btn = tk.Button(
            self.root, text="Send", command=self.send_msg, state="disabled", bg=BTN
        )
        self.send_btn.pack()

    # ----------------- UI helpers -----------------

    def write_log(self, msg: str, tag: str) -> None:
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n", tag)
        self.output.see("end")
        self.output.config(state="disabled")

    def listen_loop(self) -> None:
        while self.connected:
            msg = self.client.receive()
            if msg is None:
                break

            # ---- COLOR ROUTING (FIXED) ----
            if msg.startswith("[PRIVATE]"):
                self.write_log(msg, "private")
            elif msg.startswith("[SYSTEM]"):
                self.write_log(msg, "system")
            else:
                self.write_log(msg, "others")

        self.on_disconnect()

    # ----------------- Actions -----------------

    def send_msg(self) -> None:
        msg = self.msg_entry.get().strip()
        if not msg:
            return

        self.msg_entry.delete(0, "end")

        # ---- PRIVATE MESSAGE ----
        if msg.startswith("@"):
            parts = msg.split(" ", 1)
            target = parts[0][1:]
            content = parts[1] if len(parts) > 1 else ""

            # Local echo MUST match server protocol
            self.write_log(
                f"[PRIVATE] Me → {target}: {content}",
                "private"
            )
        else:
            self.write_log(f"[Me]: {msg}", "me")

        try:
            self.client.send(msg)
        except:
            self.on_disconnect()

    def toggle_connection(self) -> None:
        if not self.connected:
            try:
                username = self.user_entry.get().strip()
                host = self.host_entry.get().strip()
                port = int(self.port_entry.get().strip())

                if not username:
                    raise ValueError("Username cannot be empty")

                self.client.connect(host, port, username)

                self.connected = True
                self.connect_btn.config(text="Disconnect")
                self.msg_entry.config(state="normal")
                self.send_btn.config(state="normal")

                threading.Thread(
                    target=self.listen_loop, daemon=True
                ).start()

                self.write_log("[SYSTEM]: Connected", "system")

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.client.close()
            self.on_disconnect()

    def on_disconnect(self) -> None:
        if not self.connected:
            return

        self.connected = False
        self.connect_btn.config(text="Connect")
        self.msg_entry.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.write_log("[SYSTEM]: Disconnected", "system")

    def start(self) -> None:
        self.root.mainloop()
