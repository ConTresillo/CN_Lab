
---

# **Lab 5 — Socket Programming (UDP)**

## **Assignment**

**Lab Title:** Socket Programming using UDP  
**Lab Number:** Lab 5

---

## Name: S Tharun Parykshyt
## Roll No: 24BCE1119

- **In collaboration with:** Aravinda Kannan 24BCE1290(Friend)

---

## **Aim**

To understand and implement **connectionless communication** using **UDP sockets** by developing:

- a centralized message hub,
    
- a multi-user chatroom, and
    
- a basic file transfer system
    

---

## **Setup**

- **Host device:** Tharun's Desktop (acts as server)
    
- **Client device:** Aravinda’s laptop
    
- **Network:** Same Wi-Fi
    
- **Server IP:** `192.168.1.9`
    
- **Port:** `9999` (or specified per application)
    
- **Protocol:** UDP (User Datagram Protocol)
    

---

## **Code**

---

## **1) Centralized Hub**

### **Description**

A centralized hub receives messages from multiple clients and forwards them to all other connected clients.

---

### **Hub Server (Tharun's Desktop)**

```python
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

    for client in clients:
        if client != addr:
            sock.sendto(message.encode(), client)
```

---

### **Hub Client (Aravinda’s Laptop)**

```python
# hub_client.py
import socket

SERVER_IP = "192.168.1.9"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Send: ")
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))
```

---

### **Procedure (Centralized Hub)**

1. The server creates a UDP socket and binds it to the Wi-Fi IP and port.
    
2. Clients send messages to the server without establishing a connection.
    
3. The server stores client addresses when messages arrive.
    
4. Any received message is forwarded to all other clients.
    
5. Communication continues until programs are stopped manually.
    

---

## **2) Chatroom**

### **Description**

A multi-user chatroom where each user joins with a username and messages are broadcast to all participants.

---

### **Chatroom Server (Tharun's Desktop)**

```python
# chat_server.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.9", 8888))

users = {}
print("Chatroom server started")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    if addr not in users:
        users[addr] = message
        notice = f"{message} joined the chat"
        for u in users:
            sock.sendto(notice.encode(), u)
    else:
        chat_msg = f"{users[addr]}: {message}"
        for u in users:
            sock.sendto(chat_msg.encode(), u)
```

---

### **Chatroom Client**

```python
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
```

---

### **Procedure (Chatroom)**

1. The server listens for incoming messages on a UDP socket.
    
2. Each client sends their username as the first message.
    
3. The server maps each client address to its username.
    
4. All chat messages are broadcast to every connected user.
    
5. No persistent connection is maintained (UDP behavior).
    

---

## **3) File Transfer Application**

### **Description**

A simple file transfer system where a sender transmits a file to a receiver using UDP packets.

---

### **File Receiver (Host Desktop)**

```python
# file_receiver.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.1.9", 7777))

with open("received.txt", "wb") as f:
    while True:
        data, addr = sock.recvfrom(1024)
        if data == b"EOF":
            break
        f.write(data)

print("File received successfully")
```

---

### **File Sender (Friend’s Laptop)**

```python
# file_sender.py
import socket

SERVER = ("192.168.1.9", 7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open("send.txt", "rb") as f:
    while True:
        chunk = f.read(1024)
        if not chunk:
            break
        sock.sendto(chunk, SERVER)

sock.sendto(b"EOF", SERVER)
print("File sent successfully")
```

---

### **Procedure (File Transfer)**

1. The receiver creates a UDP socket and waits for incoming packets.
    
2. The sender reads the file in fixed-size chunks.
    
3. Each chunk is sent as a UDP datagram.
    
4. The receiver writes received chunks into a file.
    
5. The `"EOF"` marker indicates the end of transmission.
    

---

## **Output**

_(Paste output screenshots here)_

---

## **Conclusion**

This lab demonstrated the use of **UDP socket programming** to implement real-time communication and data transfer.  
The applications highlighted UDP’s **connectionless nature**, **low overhead**, and the need for application-level control when reliability is required.

---
