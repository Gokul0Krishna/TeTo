from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.resize(400, 100)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        input_row = QHBoxLayout(central_widget)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something...")
        
        self.send_button = QPushButton("Send")

        input_row.addWidget(self.input_field)
        input_row.addWidget(self.send_button)