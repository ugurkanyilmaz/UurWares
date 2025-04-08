import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

# Define the secret key
SECRET_KEY = "V3fq#bT.{G'eHD+=~YCgQ7"

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Button Example')
        self.setGeometry(100, 100, 300, 200)

        button = QPushButton('Click Me', self)
        button.setGeometry(100, 80, 100, 30)
        button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        QMessageBox.information(self, 'Message', 'Test message')
        QApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Initialize QApplication first

    # Check if the correct secret key is provided
    if len(sys.argv) < 2 or sys.argv[1] != SECRET_KEY:
        QMessageBox.critical(None, 'Error', 'Unauthorized access. Exiting...')
        sys.exit(1)

    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
