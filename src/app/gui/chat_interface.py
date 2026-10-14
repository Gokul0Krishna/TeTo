from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QLineEdit, QVBoxLayout, QListWidget
from PyQt6.QtCore import Qt
from cores.ai_connect import AI_response

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.resize(400, 100)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.item_list = QListWidget()
        main_layout.addWidget(self.item_list)

        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something...")
        self.send_button = QPushButton("Send")

        input_row.addWidget(self.input_field)
        input_row.addWidget(self.send_button)
        main_layout.addLayout(input_row)

        self.statusBar().showMessage("Ready")

        self.send_button.clicked.connect(self.query_process)
        self.input_field.returnPressed.connect(self.query_process)

    def query_process(self):
        """Slot: send query to local Ollama LLM and display result."""
        text = self.input_field.text().strip()
        if not text:
            self.statusBar().showMessage("Cannot send empty query!", 3000)
            return
        try:
            result = AI_response(text)
            self.item_list.addItem(f"Q: {text}\nCmd: {result.strip()}")
            self.input_field.clear()
            self.statusBar().showMessage("Done", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}", 4000)
