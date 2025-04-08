import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hesap Makinesi")
        self.setGeometry(100, 100, 300, 200)

        self.initUI()

    def initUI(self):
        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # İşlem seçimi
        self.operation_label = QLabel("Yapmak istediğiniz işlemi seçin:")
        layout.addWidget(self.operation_label)

        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Toplama", "Çıkarma", "Çarpma", "Bölme"])
        layout.addWidget(self.operation_combo)

        # Birinci sayı
        self.num1_label = QLabel("Birinci sayıyı girin:")
        layout.addWidget(self.num1_label)

        self.num1_input = QLineEdit()
        layout.addWidget(self.num1_input)

        # İkinci sayı
        self.num2_label = QLabel("İkinci sayıyı girin:")
        layout.addWidget(self.num2_label)

        self.num2_input = QLineEdit()
        layout.addWidget(self.num2_input)

        # Hesapla butonu
        self.calculate_button = QPushButton("Hesapla")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # Sonuç
        self.result_label = QLabel("Sonuç: ")
        layout.addWidget(self.result_label)

        self.central_widget.setLayout(layout)

    def calculate(self):
        try:
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())
            operation = self.operation_combo.currentText()

            if operation == "Toplama":
                result = num1 + num2
            elif operation == "Çıkarma":
                result = num1 - num2
            elif operation == "Çarpma":
                result = num1 * num2
            elif operation == "Bölme":
                if num2 != 0:
                    result = num1 / num2
                else:
                    QMessageBox.critical(self, "Hata", "Bir sayı sıfıra bölünemez.")
                    return
            else:
                QMessageBox.critical(self, "Hata", "Geçersiz işlem.")
                return

            self.result_label.setText(f"Sonuç: {result}")
        except ValueError:
            QMessageBox.critical(self, "Hata", "Lütfen geçerli bir sayı girin.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())