"""Kraken Desktop Application."""

import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class KrakenWindow(QMainWindow):
    """Main Kraken window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("🐙 Kraken")
        self.resize(1200, 800)

        label = QLabel("Welcome to Kraken 🚀")
        label.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            padding: 30px;
            """
        )

        self.setCentralWidget(label)


def main() -> None:
    """Start the application."""

    app = QApplication(sys.argv)

    window = KrakenWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()