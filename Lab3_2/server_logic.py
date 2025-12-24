import socket
import threading
from typing import Callable, List, Tuple, Optional


class ChatServer:
    """
    Handles Chat Logic: Broadcasts, Private Messages, and Shutdown.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.host = host
        self.port = port
        self.server: Optional[socket.socket] = None
        # Store clients as list of (username, socket)
        self.clients: List[Tuple[str, socket.socket]] = []
        self.running: bool = False

    def start(self, log_callback: Callable[[str], None] = print) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.running = True
        log_callback(f"[SERVER]: Listening on {self.host}:{self.port}")

        while self.running:
            try:
                conn, addr = self.server.accept()

                # Receive Username first
                try:
                    username = conn.recv(1024).decode()
                except:
                    conn.close()
                    continue

                # Add to list
                self.clients.append((username, conn))

                # Announce join
                self.broadcast(f"[SYSTEM]: {username} joined the chat.", sender_socket=None)
                log_callback(f"[SERVER]: {username} connected from {addr}")

                # Start handling thread
                threading.Thread(
                    target=self.handle_client,
                    args=(username, conn, log_callback),
                    daemon=True
                ).start()
            except OSError:
                break

    def handle_client(self, username: str, conn: socket.socket, log_callback: Callable) -> None:
        while self.running:
            try:
                data = conn.recv(1024)
                if not data: break

                msg = data.decode()

                # ---- ROUTING LOGIC ----
                if msg.startswith("@"):
                    parts = msg.split(" ", 1)
                    if len(parts) > 1:
                        target = parts[0][1:]
                        content = parts[1]
                        log_callback(f"[LOG]: {username} sent private msg to {target}")
                        self.send_private(target, username, content, conn)
                    else:
                        self.send_system_msg(conn, "Usage: @username message")
                else:
                    log_callback(f"[{username}]: {msg}")
                    self.broadcast(f"[{username}]: {msg}", sender_socket=conn)

            except:
                break

        self.remove_client(username, conn, log_callback)

    def broadcast(self, message: str, sender_socket: Optional[socket.socket]) -> None:
        for _, sock in self.clients:
            if sock != sender_socket:
                try:
                    sock.sendall(message.encode())
                except:
                    pass

    def send_private(self, target_user: str, sender_user: str, msg: str, sender_sock: socket.socket) -> None:
        target_sock = None
        for user, sock in self.clients:
            if user == target_user:
                target_sock = sock
                break

        if target_sock:
            formatted = f"(Private) [{sender_user}]: {msg}"
            try:
                target_sock.sendall(formatted.encode())
            except:
                pass
        else:
            self.send_system_msg(sender_sock, f"User '{target_user}' not found or offline.")

    def send_system_msg(self, conn: socket.socket, msg: str) -> None:
        try:
            conn.sendall(f"[SYSTEM]: {msg}".encode())
        except:
            pass

    def remove_client(self, username: str, conn: socket.socket, log_callback: Callable) -> None:
        if (username, conn) in self.clients:
            self.clients.remove((username, conn))
            log_callback(f"[SERVER]: {username} disconnected")

            # Use sender_socket=conn so the leaving user DOES NOT receive this message
            self.broadcast(f"[SYSTEM]: {username} left the chat.", sender_socket=conn)

        try:
            conn.close()
        except:
            pass

    def stop(self) -> None:
        """
        Stops the server and forcefully closes all client connections.
        """
        self.running = False

        # 1. Close Server Socket (Stops new connections)
        if self.server:
            try:
                self.server.close()
            except:
                pass

        # 2. Force Close All Client Sockets
        # We iterate over a copy [:] because remove_client modifies the list
        for username, conn in self.clients[:]:
            try:
                conn.shutdown(socket.SHUT_RDWR)  # Force interrupt recv()
                conn.close()
            except:
                pass

        self.clients.clear()