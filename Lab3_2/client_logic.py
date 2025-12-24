import socket
from typing import Optional

class ChatClient:
    def __init__(self, username: str) -> None:
        self.username = username
        self.sock: Optional[socket.socket] = None
        self.connected = False

    def connect(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        # Send username immediately on connect
        self.sock.sendall(self.username.encode())
        self.connected = True

    def send(self, msg: str) -> None:
        if self.sock: self.sock.sendall(msg.encode())

    def receive(self) -> Optional[str]:
        if not self.sock: return None
        try:
            data = self.sock.recv(1024)
            if not data: return None
            return data.decode()
        except: return None

    def close(self) -> None:
        self.connected = False
        if self.sock: self.sock.close()