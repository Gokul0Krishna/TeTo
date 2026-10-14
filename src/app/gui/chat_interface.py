from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.setGeometry(100, 100, 600, 400)
        
        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(500, 350, 80, 30)
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        # Logic to send a message
        print("Message sent!")
    