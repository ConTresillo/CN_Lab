from server_gui import ServerGUI
from server_logic import ChatServer


if __name__ == "__main__":
    server = ChatServer()
    gui = ServerGUI(server)
    gui.start()
