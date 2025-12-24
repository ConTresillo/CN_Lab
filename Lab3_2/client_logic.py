import socket
from typing import Optional

class ChatClient:
    """
    Handles networking for the chat client.
    """
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.sock: Optional[socket.socket] = None
        self.connected: bool = False

    def connect(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.sendall(self.username.encode())
        self.connected = True

    def send(self, msg: str) -> None:
        if not self.connected or not self.sock:
            raise RuntimeError("Not connected")
        try:
            self.sock.sendall(msg.encode())
        except OSError:
            self.connected = False
            raise

    def receive(self) -> Optional[str]:
        if not self.connected or not self.sock:
            return None
        try:
            data = self.sock.recv(1024)
            if not data:
                self.connected = False
                return None
            return data.decode()
        except OSError:
            self.connected = False
            return None

    def close(self) -> None:
        self.connected = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None