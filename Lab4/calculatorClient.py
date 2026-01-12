import socket

HOST = "192.168.1.8"
PORT = 8000

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))

name = input("Enter your name: ")
c.send(name.encode())

while True:
    expr = input("Enter operation (e.g., 10 + 5) or exit: ")
    if expr.lower() == "exit":
        break

    c.send(expr.encode())
    result = c.recv(1024).decode()
    print("Result:", result)

c.close()