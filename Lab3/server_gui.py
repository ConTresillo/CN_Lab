import tkinter as tk
import threading
from typing import Optional
from server_logic import EchoServer


class ServerGUI:
    """
    Tkinter GUI for Echo Server.
    Handles UI only. Server runs in background thread.
    """

    def __init__(self) -> None:
        self.server: Optional[EchoServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.running: bool = False

        # ---- Colors ----
        BG = "#1e1e1e"
        PANEL = "#252526"
        FG = "#d4d4d4"
        BTN = "#0e639c"
        ENTRY_BG = "#3c3c3c"

        self.root: tk.Tk = tk.Tk()
        self.root.title("Echo Server")
        self.root.configure(bg=BG)

        # ---- Port selection ----
        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=8)

        tk.Label(
            frame, text="Port",
            bg=PANEL, fg=FG
        ).grid(row=0, column=0, padx=5, pady=5)

        self.port_entry = tk.Entry(
            frame,
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG
        )
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)

        self.start_btn = tk.Button(
            frame,
            text="Start",
            command=self.toggle_server,
            bg=BTN,
            fg="white",
            activebackground="#1177bb",
            activeforeground="white",
            relief="flat"
        )
        self.start_btn.grid(row=1, column=0, columnspan=2, pady=8)

        # ---- Log window ----
        self.log = tk.Text(
            self.root,
            height=20,
            width=70,
            bg="#111111",
            fg=FG,
            insertbackground=FG,
            relief="flat"
        )
        self.log.pack(padx=10, pady=5)

    # ---------------- LOGGING ----------------

    def write_log(self, msg: str) -> None:
        """
        Thread-safe log writer.
        Always executed on GUI thread.
        """
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg: str) -> None:
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    # ---------------- SERVER CONTROL ----------------

    def start_server(self, port: int) -> None:
        """
        Runs in background thread.
        """
        self.server = EchoServer(port=port)
        self.server.start(log_callback=self.write_log)

    def toggle_server(self) -> None:
        if not self.running:
            try:
                port = int(self.port_entry.get().strip())
            except ValueError:
                self.write_log("[SERVER]: Invalid port")
                return

            self.server_thread = threading.Thread(
                target=self.start_server,
                args=(port,),
                daemon=True
            )
            self.server_thread.start()

            self.running = True
            self.start_btn.config(text="Stop")
            self.write_log(f"[SERVER]: Starting on port {port}")

        else:
            if self.server:
                self.server.stop()
                self.write_log("[SERVER]: Stopped")

            self.running = False
            self.start_btn.config(text="Start")

    def start(self) -> None:
        self.root.mainloop()
