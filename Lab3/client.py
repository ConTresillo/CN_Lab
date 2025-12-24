from typing import Type
from client_gui import ClientGUI


mode: str = input("Choose mode (gui/cli): ").strip().lower()

if mode == "gui":
    client_class: Type = __import__("client_logic").EchoClient
    gui: ClientGUI = ClientGUI(client_class=client_class)
    gui.start()

else:
    from client_logic import EchoClient

    username: str = input("Enter username: ")
    server_ip: str = input("Enter server IP: ")

    try:
        server_port: int = int(input("Enter server port: "))
    except ValueError:
        print("[server]: Invalid port number")
        raise SystemExit(1)

    client: EchoClient = EchoClient(username)

    try:
        client.connect(server_ip, server_port)
        print(f"[server]: Connected to {server_ip}:{server_port}")
    except Exception:
        print("[server]: Could not connect")
        raise SystemExit(1)

    try:
        while True:
            msg: str = input("Enter message (exit to quit): ")
            if msg.lower() == "exit":
                break

            # send message
            client.send(msg)

            # wait for response
            response = client.receive()
            if response is None:
                print("[server]: Disconnected")
                break

            print(f"[server]: {response}")

    except KeyboardInterrupt:
        print("\n[client]: Interrupted")

    finally:
        client.close()
