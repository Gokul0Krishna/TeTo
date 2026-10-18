from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QHBoxLayout, QWidget,
    QLineEdit, QVBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QSizePolicy, QScrollBar
)
from PyQt6.QtCore import Qt, QSize
from cores.agents.agents import Agent1


class MessageBubble(QFrame):
    """A chat bubble: QLabel styled via QSS, right-aligned for user."""

    def __init__(self, text, is_user):
        super().__init__()
        self.setObjectName("userBubble" if is_user else "agentBubble")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)

        self.label = QLabel(text)
        self.label.setObjectName("bubbleLabel")
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Spacer pushes the bubble to one side
        self.spacer_left = QWidget()
        self.spacer_right = QWidget()
        self.spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.spacer_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        if is_user:
            layout.addWidget(self.spacer_left)
            layout.addWidget(self.label)
        else:
            layout.addWidget(self.label)
            layout.addWidget(self.spacer_right)


class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Interface")
        self.resize(480, 640)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # --- Chat area ---
        self.chat_list = QListWidget()
        self.chat_list.setObjectName("chatList")
        self.chat_list.setSpacing(6)
        self.chat_list.setWordWrap(True)
        self.chat_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.chat_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_list.verticalScrollBar().setSingleStep(12)
        main_layout.addWidget(self.chat_list, stretch=1)

        # --- Input row ---
        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("inputField")
        self.input_field.setPlaceholderText("Type your message...")
        self.send_button = QPushButton("Send")

        input_row.addWidget(self.input_field, stretch=1)
        input_row.addWidget(self.send_button)
        main_layout.addLayout(input_row)

        self.statusBar().showMessage("Ready")

        self.send_button.clicked.connect(self.query_process)
        self.input_field.returnPressed.connect(self.query_process)

    def _add_message(self, text, is_user):
        """Insert a bubble as a full-width list row."""
        item = QListWidgetItem()
        bubble = MessageBubble(text, is_user)
        item.setSizeHint(bubble.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, bubble)
        self.chat_list.scrollToBottom()

    def query_process(self):
        """Send query to agent and display the result as a bubble."""
        text = self.input_field.text().strip()
        if not text:
            self.statusBar().showMessage("Cannot send an empty message!", 3000)
            return

        self._add_message(text, is_user=True)
        self.input_field.clear()
        self.send_button.setEnabled(False)
        self.statusBar().showMessage("Thinking...")

        try:
            result = Agent1(text)
            self._add_message(result.strip(), is_user=False)
            self.statusBar().showMessage("Ready", 3000)
        except Exception as e:
            self._add_message(f"⚠ Error: {e}", is_user=False)
            self.statusBar().showMessage(f"Error: {e}", 4000)
        finally:
            self.send_button.setEnabled(True)
            self.input_field.setFocus()