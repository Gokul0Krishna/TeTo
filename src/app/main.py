import sys
from PyQt6.QtWidgets import QApplication
from gui.chat_interface import ChatInterface
def run():
    app = QApplication(sys.argv)
    window = ChatInterface()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()