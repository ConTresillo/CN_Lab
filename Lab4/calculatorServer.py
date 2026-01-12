import socket
import threading

HOST = "192.168.1.8"
PORT = 8000

def calculate(expr):
    a, op, b = expr.split()
    a, b = int(a), int(b)

    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    else:
        return "Invalid operator"

def handle_client(conn, addr):
    name = conn.recv(1024).decode()
    print(f"[CONNECTED] {name} | IP={addr[0]} | Port={addr[1]}")

    while True:
        try:
            expr = conn.recv(1024).decode()
            if not expr:
                break

            print(f"{name} ({addr[0]}:{addr[1]}) requested: {expr}")
            result = calculate(expr)
            conn.send(str(result).encode())

        except:
            break

    print(f"[DISCONNECTED] {name} | IP={addr[0]} | Port={addr[1]}")
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print("Calculator Server started...")

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()