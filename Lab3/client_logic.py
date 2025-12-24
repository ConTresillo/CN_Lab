import socket
from typing import Optional


class EchoClient:
    """
    Handles all networking for the client.
    No GUI code here. Just pure business logic.
    """

    def __init__(self, username: str) -> None:
        """
        username is the name through which client joins
        sock is the socket to which client connects
        connected is status flag that validates the connection
        """
        self.username: str = username
        self.sock: Optional[socket.socket] = None
        self.connected: bool = False

    def connect(self, host: str, port: int) -> None:
        """
        Connect to the server and send username once.
        This function only connects. It does NOT listen.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.sendall(self.username.encode())
        self.connected = True

    def send(self, msg: str) -> None:
        """
        Send a message to the server.
        IMPORTANT: does NOT wait for response (non-blocking design).
        """
        if not self.connected or not self.sock:
            raise RuntimeError("Not connected to server")

        try:
            self.sock.sendall(msg.encode())
        except OSError:
            self.connected = False
            raise

    def receive(self) -> Optional[str]:
        """
        Receive ONE message from server.
        Returns:
            - string message
            - None if server disconnected
        """
        if not self.connected or not self.sock:
            return None

        try:
            data: bytes = self.sock.recv(1024)
            if not data:
                # server closed connection cleanly
                self.connected = False
                return None

            msg = data.decode()

            # control message → client should NOT echo this
            if msg == "__SERVER_SHUTDOWN__":
                self.connected = False
                return None

            return msg

        except OSError:
            self.connected = False
            return None

    def close(self) -> None:
        """
        Close socket safely.
        """
        self.connected = False
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.sock.close()
            self.sock = None
