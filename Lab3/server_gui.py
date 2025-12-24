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

        self.root: tk.Tk = tk.Tk()
        self.root.title("Echo Server")

        # ---- Port selection ----
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Port").grid(row=0, column=0)
        self.port_entry = tk.Entry(frame)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=0, column=1)

        self.start_btn = tk.Button(frame, text="Start", command=self.toggle_server)
        self.start_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # ---- Log window ----
        self.log = tk.Text(self.root, height=20, width=70)
        self.log.pack()

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
                self.write_log("[server]: Invalid port")
                return

            self.server_thread = threading.Thread(
                target=self.start_server,
                args=(port,),
                daemon=True
            )
            self.server_thread.start()

            self.running = True
            self.start_btn.config(text="Stop")
            self.write_log(f"[server]: Starting on port {port}")

        else:
            if self.server:
                self.server.stop()

            self.running = False
            self.start_btn.config(text="Start")
            self.write_log("[server]: Stopped")

    def start(self) -> None:
        self.root.mainloop()
