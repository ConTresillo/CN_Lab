import socket
import threading
from typing import Callable, List, Tuple, Optional


class EchoServer:
    """
    Echo server business logic.
    Handles networking only.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.host: str = host
        self.port: int = port
        self.server: Optional[socket.socket] = None
        self.clients: List[Tuple[str, socket.socket]] = []
        self.running: bool = False

    def start(self, log_callback: Callable[[str], None] = print) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.server.settimeout(1.0)

        self.running = True
        log_callback(f"[server]: Listening on {self.host}:{self.port}")

        while self.running:
            try:
                conn, addr = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                username = conn.recv(1024).decode()
                if not username:
                    conn.close()
                    continue
            except Exception:
                conn.close()
                continue

            self.clients.append((username, conn))
            log_callback(f"[server]: Connected to {username} at {addr}")

            threading.Thread(
                target=self.handle_client,
                args=(username, conn, log_callback),
                daemon=True
            ).start()

    def handle_client(
        self,
        username: str,
        conn: socket.socket,
        log_callback: Callable[[str], None]
    ) -> None:
        conn.settimeout(1.0)

        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                msg = data.decode()

                # NORMAL CHAT MESSAGE
                log_callback(f"[{username}]: {msg}")
                conn.sendall(msg.encode())

            except socket.timeout:
                continue
            except (ConnectionResetError, OSError):
                break

        # CLEAN DISCONNECT (not a message)
        log_callback(f"[server]: {username} disconnected")

        try:
            conn.close()
        except Exception:
            pass

        self.clients = [(u, c) for u, c in self.clients if c != conn]

    def stop(self) -> None:
        """
        Stop server and notify all clients explicitly.
        """
        self.running = False

        for _, conn in self.clients:
            try:
                conn.sendall("__SERVER_SHUTDOWN__".encode())
            except Exception:
                pass
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

        self.clients.clear()

        if self.server:
            try:
                self.server.close()
            except Exception:
                pass
            self.server = None
