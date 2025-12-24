from server_gui import ServerGUI
# Ensure server_gui.py imports ChatServer from server_logic
if __name__ == "__main__":
    gui = ServerGUI()
    gui.start()