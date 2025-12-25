import socket
from typing import Optional


class ChatClient:
    def __init__(self) -> None:
        self.sock: Optional[socket.socket] = None
        self.connected = False

    def connect(self, host: str, port: int, username: str) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.sendall(username.encode())
        self.connected = True

    def send(self, msg: str) -> None:
        if not self.sock:
            return
        self.sock.sendall(msg.encode())

    def receive(self) -> Optional[str]:
        if not self.sock:
            return None
        try:
            data = self.sock.recv(1024)
            if not data:
                return None
            return data.decode()
        except:
            return None

    def close(self) -> None:
        self.connected = False
        if self.sock:
            self.sock.close()
            self.sock = None
