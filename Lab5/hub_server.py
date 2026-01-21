# hub_server.py
import socket

SERVER_IP = "192.168.1.9"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

clients = set()

print("Centralized Hub running...")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    if addr not in clients:
        clients.add(addr)
        print(f"New client joined: {addr}")

    print(f"Received from {addr}: {message}")

    for client in clients:
        if client != addr:
            sock.sendto(message.encode(), client)
