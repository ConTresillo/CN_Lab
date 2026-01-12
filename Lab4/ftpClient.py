import socket
import os

HOST = "192.168.1.8"
PORT = 7000

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))

name = input("Enter your name: ")
c.send(name.encode())

filename = input("Enter file name to send: ")
c.send(filename.encode())

with open(filename, "rb") as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        c.send(data)

print("File sent successfully")
c.close()