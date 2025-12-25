import socket
import threading
from typing import Callable, List, Tuple, Optional


class ChatServer:
    """
    Handles chat networking and routing logic.
    No GUI knowledge.
    """

    def __init__(self) -> None:
        self.server: Optional[socket.socket] = None
        self.clients: List[Tuple[str, socket.socket]] = []
        self.running = False

    def start(
        self,
        host: str,
        port: int,
        log_callback: Callable[[str], None] = print
    ) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.running = True

        log_callback(f"[SERVER]: Listening on {host}:{port}")

        while self.running:
            try:
                conn, addr = self.server.accept()

                try:
                    username = conn.recv(1024).decode()
                except:
                    conn.close()
                    continue

                self.clients.append((username, conn))
                self.broadcast(
                    f"[SYSTEM]: {username} joined the chat.",
                    sender_socket=None
                )

                log_callback(f"[SERVER]: {username} connected from {addr}")

                threading.Thread(
                    target=self.handle_client,
                    args=(username, conn, log_callback),
                    daemon=True
                ).start()

            except OSError:
                break

    def handle_client(
        self,
        username: str,
        conn: socket.socket,
        log_callback: Callable[[str], None]
    ) -> None:
        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                msg = data.decode()

                if msg.startswith("@"):
                    parts = msg.split(" ", 1)
                    if len(parts) > 1:
                        target = parts[0][1:]
                        content = parts[1]
                        log_callback(
                            f"[LOG]: {username} → (private) {target}"
                        )
                        self.send_private(target, username, content, conn)
                    else:
                        self.send_system_msg(
                            conn,
                            "Usage: @username message"
                        )
                else:
                    log_callback(f"[{username}]: {msg}")
                    self.broadcast(
                        f"[{username}]: {msg}",
                        sender_socket=conn
                    )

            except:
                break

        self.remove_client(username, conn, log_callback)

    # ---------------- Messaging ----------------

    def broadcast(
        self,
        message: str,
        sender_socket: Optional[socket.socket]
    ) -> None:
        for _, sock in self.clients:
            if sock != sender_socket:
                try:
                    sock.sendall(message.encode())
                except:
                    pass

    def send_private(
        self,
        target_user: str,
        sender_user: str,
        msg: str,
        sender_sock: socket.socket
    ) -> None:
        for user, sock in self.clients:
            if user == target_user:
                try:
                    sock.sendall(
                        f"(Private) [{sender_user}]: {msg}".encode()
                    )
                except:
                    pass
                return

        self.send_system_msg(
            sender_sock,
            f"User '{target_user}' not found or offline."
        )

    def send_system_msg(self, conn: socket.socket, msg: str) -> None:
        try:
            conn.sendall(f"[SYSTEM]: {msg}".encode())
        except:
            pass

    # ---------------- Cleanup ----------------

    def remove_client(
        self,
        username: str,
        conn: socket.socket,
        log_callback: Callable[[str], None]
    ) -> None:
        if (username, conn) in self.clients:
            self.clients.remove((username, conn))
            log_callback(f"[SERVER]: {username} disconnected")
            self.broadcast(
                f"[SYSTEM]: {username} left the chat.",
                sender_socket=conn
            )

        try:
            conn.close()
        except:
            pass

    def stop(self) -> None:
        self.running = False

        if self.server:
            try:
                self.server.close()
            except:
                pass

        for _, conn in self.clients[:]:
            try:
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
            except:
                pass

        self.clients.clear()
