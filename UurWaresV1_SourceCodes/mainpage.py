from PyQt6 import QtCore, QtGui, QtWidgets
import subprocess
import sys
from database import db_connection
from uimainpage import Ui_MainWindow
import requests
import os
import json

# Constants for paths and URLs
LOCAL_FEATURES_PATH = "C:\\UurWaresv1\\features"
VERSION_FILE_PATH = "C:\\UurWaresv1\\version.json"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ugurkanyilmaz/UurWares/main/version.json"
GITHUB_BASE_URL = "https://raw.githubusercontent.com/ugurkanyilmaz/UurWares/main/"
SECRET_KEY = "secret key"

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, user_id, username):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(f"UurWares, {username}") 
        self.ui.lblusername.setText(f"{username}")
        self.user_id = user_id 
        self.cursor = db_connection.cursor()
        self.display_features()
        self.check_and_download_features()

        # Connect the clicked signal of applist to display_instructions
        self.ui.applist.clicked.connect(self.display_instructions)
        self.ui.btnstart.clicked.connect(self.feature_start)

    def get_features(self):
        self.cursor.execute("""
            SELECT f.name FROM features f
            JOIN user_features uf ON f.feature_id = uf.feature_id
            WHERE uf.user_id = %s
        """, (self.user_id,))
        features = self.cursor.fetchall()
        return features

    def display_features(self):
        features = self.get_features()

        # Using QStandardItemModel to display features in QListView
        model = QtGui.QStandardItemModel()

        for feature in features:
            item = QtGui.QStandardItem(feature[0])
            model.appendRow(item)

        # Connect the model to the QListView.
        self.ui.applist.setModel(model)
    
    def display_instructions(self):
        feature_name = self.ui.applist.currentIndex().data()
        if not feature_name:
            self.ui.instructionBox.setText("No feature selected.")
            return

        self.cursor.execute("""
            SELECT instructions FROM features WHERE name = %s
        """, (feature_name,))
        instructions = self.cursor.fetchone()
        if instructions:
            self.ui.instructionBox.setText(instructions[0])
        else:
            self.ui.instructionBox.setText("No instructions available.")
    
    def feature_start(self):
        feature_name = self.ui.applist.currentIndex().data()
        if not feature_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a feature to start.")
            return

        local_path = os.path.join(LOCAL_FEATURES_PATH, feature_name)
        if os.path.exists(local_path):
            QtWidgets.QMessageBox.information(self, "Feature Starter", f"Starting {feature_name}")
            try:
                if local_path.endswith(".py"):
                    subprocess.Popen([sys.executable, local_path, SECRET_KEY])
                elif local_path.endswith(".exe"):
                    subprocess.Popen([local_path, SECRET_KEY], shell=True)
                else:
                    subprocess.Popen(local_path, shell=True)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to start feature: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Feature is not found: {feature_name}")
    
    def check_and_download_features(self):
        # Kullanıcıya tanımlı özellikleri al
        user_features = [f[0] for f in self.get_features()]
        if not user_features:
            print("Kullanıcıya tanımlı özellik yok, indirme yapılmayacak.")
            return

        if not os.path.exists(LOCAL_FEATURES_PATH):
            os.makedirs(LOCAL_FEATURES_PATH)

        try:
            response = requests.get(GITHUB_VERSION_URL)
            if response.status_code == 200:
                remote_version_data = response.json()

                local_version_data = {}
                if os.path.exists(VERSION_FILE_PATH):
                    with open(VERSION_FILE_PATH, "r") as f:
                        local_version_data = json.load(f)

                for feature, version in remote_version_data.get("features", {}).items():
                    # Sadece kullanıcıya tanımlı özellikleri indir
                    if feature not in user_features:
                        continue

                    local_feature_path = os.path.join(LOCAL_FEATURES_PATH, feature)
                    if feature not in local_version_data or local_version_data.get(feature) != version:
                        feature_url = GITHUB_BASE_URL + feature
                        feature_response = requests.get(feature_url)
                        if feature_response.status_code == 200:
                            with open(local_feature_path, "wb") as f:
                                f.write(feature_response.content)
                            local_version_data[feature] = version

                with open(VERSION_FILE_PATH, "w") as f:
                    json.dump(local_version_data, f, indent=4)
        except Exception as e:
            print(f"Update check failed: {str(e)}")
