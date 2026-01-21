# COMPUTER NETWORKS LAB  
## EXPERIMENT NO: 4  
### Socket Programming – Calculator and File Transfer using TCP  

**Name:** Aravinda Kannan K.S  
**Register No:** 24BCE1290  

---

## AIM

To implement TCP based Client–Server applications using Python Socket Programming for:
1. File Transfer service  
2. Remote Calculator service  

---

## THEORY

Socket programming enables communication between two systems over a network.  
Transmission Control Protocol (TCP) is a connection-oriented and reliable protocol that ensures correct and ordered delivery of data without loss.

---

## SYSTEM ARCHITECTURE

### File Transfer Module  
File Client → File Server → Save file  
### Calculator Module  
Client → Calculator Server → Result back to Client  

---

## NETWORK SETUP

| Component            | IP Address   | Port |
| -------------------- | ------------ | ---- |
| File Transfer Server | 192.168.1.8  | 7000 |
| Calculator Server    | 192.168.1.8  | 8000 |
| Client               | Same Network | Any  |

---

## LAB 4.2 – CALCULATOR USING TCP  
### CODE EXPLANATION

**Server Side Explanation**

- The socket module is used to create a TCP socket for network communication.  
- The threading module allows the server to handle multiple clients simultaneously.  
- The server binds to a specific IP address and port and listens for incoming connections.  
- When a client connects, a new thread is created for that client.  
- The server receives the client name for identification.  
- Arithmetic expressions sent by the client are received as strings.  
- The expression is split into operands and operator.  
- Based on the operator, the corresponding arithmetic operation is performed.  
- The calculated result is sent back to the client.  
- The connection is closed when the client exits.

**Client Side Explanation**

- The client creates a TCP socket and connects to the server using IP and port.  
- The client sends the user name to the server.  
- The client repeatedly sends arithmetic expressions in the format: number operator number.  
- The server response containing the result is received and displayed.  
- The client terminates the connection when the user chooses to exit.


## Output
### Aravinda's Screen
![[Pasted image 20260112220759.png]]
### Tharun's Server
![[Pasted image 20260112224446.png]]
### Tharun's Screen
![[Pasted image 20260112224506.png]]

---

## LAB 4.1 – FILE TRANSFER USING TCP  
### CODE EXPLANATION

**Server Side Explanation**

- The server creates a TCP socket and binds it to a specified IP address and port.  
- The server listens continuously for client connections.  
- For each client, a new thread is created to handle the file transfer.  
- The server receives the client name and file name.  
- A new file is created on the server using the received file name.  
- File data is received in binary chunks and written to the file.  
- The server closes the connection after the complete file is received.

**Client Side Explanation**

- The client creates a TCP socket and connects to the file server.  
- The client sends the user name and file name to the server.  
- The file is opened in binary read mode.  
- File data is read in fixed-size chunks and sent to the server.  
- After sending the complete file, the client closes the connection.

---

## OBSERVATION

- Multiple calculator clients were served concurrently.  
- Accurate results were received for all arithmetic operations.  
- The file transfer completed successfully without data corruption.  
- The server correctly saved the received file.
## Setup
### Aravinda : Client
### Tharun : Server
## Code
```python
#server.py

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
```

```python
#client.py

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
```
## Code Explanation

## Output
### Aravind sends file demo.txt
![[Pasted image 20260112225042.png]]
### Tharun receives the file demo.txt
![[Pasted image 20260112225113.png]]
---

## RESULT

The TCP based Calculator and File Transfer applications were successfully implemented using Python Socket Programming.

---

## CONCLUSION

This experiment demonstrated client–server communication using TCP sockets, multithreading for handling multiple clients, and reliable binary file transfer over a network.