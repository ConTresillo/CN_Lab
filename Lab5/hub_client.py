# hub_client.py
import socket

SERVER_IP = " 192.168.1.9"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Send: ")
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

    sock.settimeout(1)
    try:
        data, _ = sock.recvfrom(1024)
        print("Received:", data.decode())
    except:
        pass
