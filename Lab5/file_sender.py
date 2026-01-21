# file_sender.py
import socket

SERVER = ("192.168.1.9", 7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

filename = "send.txt"

with open(filename, "rb") as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        sock.sendto(data, SERVER)

sock.sendto(b"EOF", SERVER)
print("File sent")
