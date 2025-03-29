import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

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
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())