import tkinter as tk
import threading
from server_logic import ChatServer


class ChatServerGUI:
    def __init__(self) -> None:
        self.server = None
        self.root = tk.Tk()
        self.root.title("Chat Room Server")

        self.start_btn = tk.Button(self.root, text="Start Server", command=self.toggle_server)
        self.start_btn.pack(pady=10)

        self.log = tk.Text(self.root, height=20, width=50)
        self.log.pack()

    def write_log(self, msg: str) -> None:
        self.root.after(0, lambda: self.log.insert("end", msg + "\n"))

    def toggle_server(self) -> None:
        if not self.server:
            self.server = ChatServer()
            threading.Thread(target=self.server.start, args=(self.write_log,), daemon=True).start()
            self.start_btn.config(text="Stop Server")
        else:
            self.server.stop()
            self.server = None
            self.start_btn.config(text="Start Server")
            self.write_log("[SERVER]: Stopped")

    def start(self) -> None:
        self.root.mainloop()