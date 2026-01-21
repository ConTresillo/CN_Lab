# file_receiver.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((" 192.168.1.9", 7777))

with open("received.txt", "wb") as f:
    while True:
        data, addr = sock.recvfrom(1024)
        if data == b"EOF":
            break
        f.write(data)

print("File received")
