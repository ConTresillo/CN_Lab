from client_gui import ClientGUI
from client_logic import ChatClient # Updated import

if __name__ == "__main__":
    gui = ClientGUI(client_class=ChatClient)
    gui.start()