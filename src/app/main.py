import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from gui.chat_interface import ChatInterface


def run():
    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "styles" / "style.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text())

    window = ChatInterface()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()