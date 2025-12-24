from server_gui import ServerGUI


if __name__ == "__main__":
    mode: str = input("Choose mode (gui/cli): ").strip().lower()

    if mode == "gui":
        gui: ServerGUI = ServerGUI()
        gui.start()

    else:
        from server_logic import EchoServer

        try:
            port: int = int(input("Enter server port to listen on: "))
        except ValueError:
            print("[server]: Invalid port number")
            raise SystemExit(1)

        server: EchoServer = EchoServer(port=port)

        try:
            server.start()
        except KeyboardInterrupt:
            print("\n[server]: Shutting down")
        finally:
            server.stop()
