from client_gui import ClientGUI
from client_logic import ChatClient


if __name__ == "__main__":
    client = ChatClient()
    gui = ClientGUI(client)
    gui.start()
