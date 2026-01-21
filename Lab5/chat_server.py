# chat_server.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.9", 8888))

users = {}

print("Chatroom Server Started")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    if addr not in users:
        users[addr] = message
        join_msg = f"{message} joined the chat"
        for u in users:
            sock.sendto(join_msg.encode(), u)
    else:
        full_msg = f"{users[addr]}: {message}"
        for u in users:
            sock.sendto(full_msg.encode(), u)
