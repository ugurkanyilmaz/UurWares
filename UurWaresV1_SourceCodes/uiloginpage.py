from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 350)
        MainWindow.setFixedSize(400, 350)

        # Koyu Tema Stili
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border-radius: 10px;
            }
            QLineEdit {
                background-color: #3b3b3b;
                color: #ffffff;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #555;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
            }
        """)  

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, -20, 191, 180))
        self.label.setObjectName("logoLabel")
        self.label.setPixmap(QtGui.QPixmap("UurWaresLogo.png"))
        self.label.setScaledContents(True)

        self.lblUsername = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblUsername.setGeometry(QtCore.QRect(50, 140, 80, 25))
        self.lblUsername.setObjectName("lblUsername")
        self.lblUsername.setText("Username:")

        self.lineUsername = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineUsername.setGeometry(QtCore.QRect(150, 140, 200, 25))
        self.lineUsername.setObjectName("lineUsername")
        self.lineUsername.setPlaceholderText("Enter your username")
        self.lineUsername.setStyleSheet("background-color: #3b3b3b; color: #ffffff; border-radius: 5px; padding: 5px;")

        self.lblPass = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblPass.setGeometry(QtCore.QRect(50, 180, 80, 25))
        self.lblPass.setObjectName("lblPass")
        self.lblPass.setText("Password:")

        self.linePass = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.linePass.setGeometry(QtCore.QRect(150, 180, 200, 25))
        self.linePass.setObjectName("linePass")
        self.linePass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.linePass.setPlaceholderText("Enter your password")
        self.linePass.setStyleSheet("background-color: #3b3b3b; color: #ffffff; border-radius: 5px; padding: 5px;")

        # Şifre gösterme/gizleme butonu
        self.btnShowPass = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnShowPass.setGeometry(QtCore.QRect(360, 180, 25, 25))
        self.btnShowPass.setObjectName("btnShowPass")
        self.btnShowPass.setText("👁")
        self.btnShowPass.setStyleSheet("""
            background-color: #555;
            color: #fff;
            border-radius: 5px;
        """)
        self.btnShowPass.clicked.connect(self.toggle_password)

        self.btnLogin = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnLogin.setGeometry(QtCore.QRect(100, 240, 200, 40))
        self.btnLogin.setObjectName("btnLogin")
        self.btnLogin.setText("Login")
        self.btnLogin.setStyleSheet("background-color: #0078d7; color: white; border-radius: 5px; font-size: 14px;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UurWares"))
        MainWindow.setWindowIcon(QtGui.QIcon("UurWaresLogo.ico"))

    def toggle_password(self):
        if self.linePass.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.linePass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.linePass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
