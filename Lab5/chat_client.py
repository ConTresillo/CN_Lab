# chat_client.py
import socket
import threading

SERVER = ("192.168.1.9", 8888)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = input("Enter username: ")
sock.sendto(name.encode(), SERVER)

def receive():
    while True:
        data, _ = sock.recvfrom(1024)
        print(data.decode())

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    sock.sendto(msg.encode(), SERVER)
