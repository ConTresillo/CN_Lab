import tkinter as tk
import threading
from typing import Optional


class ServerGUI:
    """
    Tkinter GUI for Chat Server.
    No server construction inside.
    """

    def __init__(self, server) -> None:
        self.server = server
        self.server_thread: Optional[threading.Thread] = None
        self.running = False

        # ---- Dark Theme ----
        BG = "#1e1e1e"
        PANEL = "#252526"
        FG = "#d4d4d4"
        BTN = "#0e639c"
        BTN_STOP = "#B00020"
        ENTRY_BG = "#3c3c3c"

        self.root = tk.Tk()
        self.root.title("Chat Server")
        self.root.configure(bg=BG)

        frame = tk.Frame(self.root, bg=PANEL)
        frame.pack(pady=10, fill="x", padx=10)

        tk.Label(frame, text="Host", bg=PANEL, fg=FG).pack(side="left", padx=5)
        self.host_entry = tk.Entry(
            frame, bg=ENTRY_BG, fg=FG, width=12
        )
        self.host_entry.insert(0, "0.0.0.0")
        self.host_entry.pack(side="left", padx=5)

        tk.Label(frame, text="Port", bg=PANEL, fg=FG).pack(side="left", padx=5)
        self.port_entry = tk.Entry(
            frame, bg=ENTRY_BG, fg=FG, width=8
        )
        self.port_entry.insert(0, "55555")
        self.port_entry.pack(side="left", padx=5)

        self.start_btn = tk.Button(
            frame,
            text="Start Server",
            command=self.toggle_server,
            bg=BTN,
            fg="white",
            relief="flat",
            padx=12
        )
        self.start_btn.pack(side="left", padx=20)

        self.log = tk.Text(
            self.root,
            height=20,
            width=70,
            bg="#111111",
            fg=FG,
            insertbackground="white",
            state="disabled"
        )
        self.log.pack(padx=10, pady=10)

    # ---------------- Logging ----------------

    def write_log(self, msg: str) -> None:
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg: str) -> None:
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # ---------------- Control ----------------

    def toggle_server(self) -> None:
        if not self.running:
            try:
                host = self.host_entry.get().strip()
                port = int(self.port_entry.get().strip())
            except ValueError:
                self.write_log("[ERROR]: Invalid host or port")
                return

            self.server_thread = threading.Thread(
                target=self.server.start,
                args=(host, port, self.write_log),
                daemon=True
            )
            self.server_thread.start()

            self.running = True
            self.start_btn.config(text="Stop Server", bg="#B00020")
        else:
            self.server.stop()
            self.running = False
            self.start_btn.config(text="Start Server", bg="#0e639c")
            self.write_log("[SERVER]: Stopped")

    def start(self) -> None:
        self.root.mainloop()
