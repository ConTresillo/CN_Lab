import tkinter as tk
import threading
from typing import Optional
from server_logic import ChatServer  # Ensure this matches your logic filename


class ServerGUI:
    """
    Tkinter GUI for Chat Server.
    Theme: Dark Mode (Black/Gray).
    """

    def __init__(self) -> None:
        self.server: Optional[ChatServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.running: bool = False

        # ---- Dark Theme Colors ----
        BG = "#1e1e1e"
        PANEL = "#252526"
        FG = "#d4d4d4"
        BTN = "#0e639c"  # Blue button
        BTN_ACTIVE = "#1177bb"
        ENTRY_BG = "#3c3c3c"

        self.root: tk.Tk = tk.Tk()
        self.root.title("Chat Server")
        self.root.configure(bg=BG)

        # ---- Control Frame ----
        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=10, fill="x", padx=10)

        tk.Label(frame, text="Port", bg=PANEL, fg=FG).pack(side="left", padx=5)

        self.port_entry = tk.Entry(frame, bg=ENTRY_BG, fg=FG, insertbackground="white", width=10)
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(side="left", padx=5)

        self.start_btn = tk.Button(
            frame,
            text="Start Server",
            command=self.toggle_server,
            bg=BTN,
            fg="white",
            activebackground=BTN_ACTIVE,
            activeforeground="white",
            relief="flat",
            padx=10
        )
        self.start_btn.pack(side="left", padx=20)

        # ---- Log Window ----
        self.log = tk.Text(
            self.root,
            height=20,
            width=70,
            bg="#111111",  # Deep black for logs
            fg=FG,
            insertbackground="white",
            relief="flat",
            state="disabled"
        )
        self.log.pack(padx=10, pady=10)

    # ---------------- LOGGING ----------------

    def write_log(self, msg: str) -> None:
        """Thread-safe logging."""
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg: str) -> None:
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # ---------------- CONTROL ----------------

    def toggle_server(self) -> None:
        if not self.running:
            try:
                port = int(self.port_entry.get().strip())
            except ValueError:
                self.write_log("[ERROR]: Invalid port")
                return

            self.server = ChatServer(port=port)
            self.server_thread = threading.Thread(
                target=self.server.start,
                args=(self.write_log,),
                daemon=True
            )
            self.server_thread.start()

            self.running = True
            self.start_btn.config(text="Stop Server", bg="#B00020")  # Red color for stop
        else:
            if self.server:
                self.server.stop()

            self.running = False
            self.start_btn.config(text="Start Server", bg="#0e639c")  # Back to Blue
            self.write_log("[SERVER]: Stopped")

    def start(self) -> None:
        self.root.mainloop()