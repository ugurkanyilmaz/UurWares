"""
UurWares Client - Login and Application Entry Point

Author: Uğurkan Yılmaz [ugurkanyilmaz]
Date: 2025-05-16

Purpose:
--------
This file serves as the entry point for the UurWares client application. It manages the user login process, version checking, and the transition to the main application window after successful authentication.

Key Features:
-------------
- User Login: Presents a PyQt6-based login window, authenticates users against a PostgreSQL database, and handles login events.
- Version Check: Compares the local client version with the remote version (from AWS S3) before allowing access, ensuring users always run the latest approved version.
- Updater Integration: If a new version is available, launches the updater and exits the application.
- Secure Transition: On successful login, securely passes user information to the main application window (feature_start.py).
- User Experience: Provides clear feedback for login success/failure and missing updater scenarios.

About UurWares:
---------------
UurWares is a desktop platform for distributing, updating, and managing user-specific features (tools, scripts, or executables) in a secure and controlled environment. This file is the first step in the user journey, ensuring only authorized and up-to-date users can access the platform.

"""

"""
Entry point for the application.
- Displays the login window using the custom UI from uiloginpage.py.
- Checks for application updates before login.
- Authenticates users against the database.
- On successful login, opens the main application window (feature_start.py).
"""

import sys
from PyQt6 import QtWidgets
from uiloginpage import Ui_MainWindow
from database import db_connection
from feature_start import MainApp
import os
import json
import requests


VERSION_URL = "https://uurwares.s3.eu-north-1.amazonaws.com/version.json"
LOCAL_VERSION_FILE = os.path.join(os.getcwd(), "version.json")

    

def get_current_version():
    try:
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as version_file:
                version_data = json.load(version_file)
                return version_data.get("client", {}).get("version", "1")
        return "1"
    except Exception as e:
        print(f"Error - Unable to read local version: {e}")
        return "1"
    
    
def check_for_updates():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            remote_version_data = response.json()
            remote_version = remote_version_data.get("client", {}).get("version", None)
            return remote_version
        print("Unable to fetch the latest version information.")
        return None
    except Exception as e:
        print(f"Version check error: {e}")
        return None

class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cursor = db_connection.cursor()
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.linePass.returnPressed.connect(self.login)


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

            self.hide()  # self.close() yerine self.hide() kullanıldı
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Wrong username or password!")


def app():
    current_version = get_current_version()
    print(f"Local version: {current_version}")
    latest_version = check_for_updates()
    print(f"Remote version: {latest_version}")
    if latest_version and latest_version != current_version:
        updater_path = os.path.join(os.getcwd(), "updater.exe")
        if os.path.exists(updater_path):
            os.startfile(updater_path)
            sys.exit(0)  # Uygulamayı kapat
        else:
            app = QtWidgets.QApplication(sys.argv)
            QtWidgets.QMessageBox.warning(None, "Updater Not Found", "updater.exe bulunamadı.")
            sys.exit(0)
    # Sürüm güncel, uygulamaya devam et
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec())

app()
