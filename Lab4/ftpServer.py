import socket
import threading

HOST = "192.168.1.8"
PORT = 7000

def handle_client(conn, addr):
    name = conn.recv(1024).decode()
    print(f"[CONNECTED] {name} | IP={addr[0]} | Port={addr[1]}")

    filename = conn.recv(1024).decode()
    print(f"[RECEIVING FILE] {filename} from {name} ({addr[0]}:{addr[1]})")

    with open("received_" + filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"[FILE RECEIVED] {filename} from {name}")
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print("File Transfer Server started...")

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()