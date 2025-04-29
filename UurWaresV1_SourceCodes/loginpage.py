import sys
import mysql.connector
from PyQt6 import QtWidgets
from uiloginpage import Ui_MainWindow
from database import db_connection
from mainpage import MainApp


class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cursor = db_connection.cursor()
        self.ui.btnLogin.clicked.connect(self.login)


    def login(self):     # Get the username and password from the input fields
        username = self.ui.lineUsername.text()
        password = self.ui.linePass.text()
                
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        
        if user:
            QtWidgets.QMessageBox.information(self, "Succesful", "Login Succesful!")

            user_id = user[0]  
            username = user[1]  

            # Send the user_id and username to the main window
            self.main_window = MainApp(user_id, username)
            self.main_window.show()

            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Wrong username or password!")


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec())

app()
