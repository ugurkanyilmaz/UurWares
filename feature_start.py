"""
Implements the main application logic after user login.
- Loads user-specific features from the database.
- Checks for missing or outdated features and downloads them from a remote server.
- Handles feature launching (Python scripts or executables).
- Displays instructions and progress to the user.
- Uses logging for error tracking and debugging.
"""

from PyQt6 import QtCore, QtGui, QtWidgets
import subprocess
import sys
from database import db_connection
from feature_start_ui import Ui_MainWindow
import requests
import os
import json
import logging

# Constants for paths and URLs
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_FEATURES_PATH = os.path.join(BASE_DIR, "features")
VERSION_FILE_PATH = os.path.join(BASE_DIR, "version.json")
VERSION_URL = "https://uurwares.s3.eu-north-1.amazonaws.com/version.json"
FEATURES_URL = "https://uurwares.s3.eu-north-1.amazonaws.com/"
SECRET_KEY = "secret_key_here"

# Log dosyası ayarları
try:
    if getattr(sys, 'frozen', False):
        LOG_DIR = os.path.dirname(sys.executable)
    else:
        LOG_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(LOG_DIR, "application.log")
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logging.info("Logging started successfully.")
except Exception as e:
    print(f"Logging could not be started: {e}")

class FeatureDownloader(QtCore.QThread):
    progress = QtCore.pyqtSignal(str)

    def __init__(self, missing_features):
        super().__init__()
        self.missing_features = missing_features

    def run(self):
        try:
            logging.info("FeatureDownloader thread started running.")
            if not os.path.exists(LOCAL_FEATURES_PATH):
                os.makedirs(LOCAL_FEATURES_PATH)
            if not self.missing_features:
                self.progress.emit("All features are up to date.")
                logging.info("All features are up to date.")
                return
            self.progress.emit("Downloading missing features...")
            logging.info(f"Downloading missing features: {self.missing_features}")

            # Remote version verilerini başta çek
            remote_version_data = {}
            try:
                response = requests.get(VERSION_URL)
                if response.status_code == 200:
                    remote_version_data = response.json()
            except Exception as e:
                logging.error(f"Remote version fetch failed in downloader: {str(e)}")
                remote_version_data = {}
            remote_features = remote_version_data.get("features", {})

            for feature_name in self.missing_features:
                remote_path = f"{FEATURES_URL}{feature_name}"
                local_path = os.path.join(LOCAL_FEATURES_PATH, feature_name)
                local_dir = os.path.dirname(local_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                try:
                    response = requests.get(remote_path, stream=True)
                    if response.status_code == 200:
                        total_length = response.headers.get('content-length')
                        if total_length is None:
                            with open(local_path, "wb") as f:
                                f.write(response.content)
                            msg = f"{feature_name} downloaded successfully. (100%)"
                            self.progress.emit(msg)
                            logging.info(msg)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            with open(local_path, "wb") as f:
                                for data in response.iter_content(chunk_size=4096):
                                    dl += len(data)
                                    f.write(data)
                                    percent = int(100 * dl / total_length)
                                    msg = f"{feature_name} downloading... %{percent}"
                                    self.progress.emit(msg)
                            msg = f"{feature_name} downloaded successfully. (100%)"
                            self.progress.emit(msg)
                            logging.info(msg)
                        # --- VERSİYON GÜNCELLEME ---
                        try:
                            # Local version.json oku veya oluştur
                            if os.path.exists(VERSION_FILE_PATH):
                                with open(VERSION_FILE_PATH, "r", encoding="utf-8") as vf:
                                    local_version_data = json.load(vf)
                            else:
                                local_version_data = {"features": {}, "client": {"version": "1"}}
                            # Remote'dan feature versiyonunu al
                            remote_version = remote_features.get(feature_name)
                            if remote_version is not None:
                                if "features" not in local_version_data:
                                    local_version_data["features"] = {}
                                local_version_data["features"][feature_name] = remote_version
                                # Dosyayı güncelle
                                with open(VERSION_FILE_PATH, "w", encoding="utf-8") as vf:
                                    json.dump(local_version_data, vf, indent=4, ensure_ascii=False)
                                logging.info(f"Local version.json updated for {feature_name} to version {remote_version}")
                        except Exception as e:
                            logging.error(f"Failed to update local version.json for {feature_name}: {str(e)}")
                    else:
                        msg = f"Failed to download {feature_name}: {response.status_code}"
                        self.progress.emit(msg)
                        logging.error(msg)
                except Exception as e:
                    msg = f"Error downloading {feature_name}: {str(e)}"
                    self.progress.emit(msg)
                    logging.error(msg)
            logging.info("FeatureDownloader thread finished.")
        except Exception as e:
            logging.critical(f"FeatureDownloader thread crashed: {str(e)}")
            self.progress.emit(f"Critical error in downloader thread: {str(e)}")

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, user_id, username):
        try:
            super(MainApp, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle(f"UurWares, {username}")
            self.ui.lblusername.setText(f"{username}")
            self.user_id = user_id
            self.cursor = db_connection.cursor()
            self.display_features()
            self.start_feature_download()
            self.ui.applist.clicked.connect(self.display_instructions)
            self.ui.btnstart.clicked.connect(self.feature_start)
            logging.info(f"MainApp initialized for user: {username}")
        except Exception as e:
            logging.critical(f"MainApp initialization failed: {str(e)}")
            print(f"MainApp initialization failed: {str(e)}")
            raise

    def get_features(self):
        try:
            self.cursor.execute("""
                SELECT f.name FROM features f
                JOIN user_features uf ON f.feature_id = uf.feature_id
                WHERE uf.user_id = %s
            """, (self.user_id,))
            features = self.cursor.fetchall()
            logging.info(f"Fetched features for user {self.user_id}: {features}")
            return features
        except Exception as e:
            logging.error(f"Error fetching features: {str(e)}")
            return []

    def display_features(self):
        try:
            features = self.get_features()
            model = QtGui.QStandardItemModel()
            for feature in features:
                item = QtGui.QStandardItem(feature[0])
                model.appendRow(item)
            self.ui.applist.setModel(model)
            logging.info("Features displayed in applist.")
        except Exception as e:
            logging.error(f"Error displaying features: {str(e)}")

    def display_instructions(self):
        try:
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
            logging.info(f"Displayed instructions for feature: {feature_name}")
        except Exception as e:
            logging.error(f"Error displaying instructions: {str(e)}")

    def feature_start(self):
        try:
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
                    logging.info(f"Started feature: {feature_name}")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to start feature: {str(e)}")
                    logging.error(f"Failed to start feature {feature_name}: {str(e)}")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Feature is not found: {feature_name}")
                logging.warning(f"Feature not found: {feature_name}")
        except Exception as e:
            logging.error(f"Error in feature_start: {str(e)}")

    def check_for_updates(self):
        try:
            features = self.get_features()
            missing_features = []
            local_version_data = {}
            if os.path.exists(VERSION_FILE_PATH):
                with open(VERSION_FILE_PATH, "r") as f:
                    local_version_data = json.load(f)
            remote_version_data = {}
            try:
                response = requests.get(VERSION_URL)
                if response.status_code == 200:
                    remote_version_data = response.json()
            except Exception as e:
                self.ui.progressBox.append(f"Remote version fetch failed: {str(e)}")
                logging.error(f"Remote version fetch failed: {str(e)}")
                return []
            local_features = local_version_data.get("features", {})
            remote_features = remote_version_data.get("features", {})
            for feature in features:
                feature_name = feature[0]
                local_path = os.path.join(LOCAL_FEATURES_PATH, feature_name)
                local_version = local_features.get(feature_name)
                remote_version = remote_features.get(feature_name)
                if not os.path.exists(local_path) or local_version != remote_version:
                    if os.path.exists(local_path):
                        try:
                            os.remove(local_path)
                            self.ui.progressBox.append(f"{feature_name} deleted due to version mismatch.")
                            logging.info(f"{feature_name} deleted due to version mismatch.")
                        except Exception as e:
                            self.ui.progressBox.append(f"{feature_name} could not be deleted: {str(e)}")
                            logging.error(f"{feature_name} could not be deleted: {str(e)}")
                    missing_features.append(feature_name)
            logging.info(f"Missing features: {missing_features}")
            return missing_features
        except Exception as e:
            logging.error(f"Error in check_for_updates: {str(e)}")
            return []

    def start_feature_download(self):
        try:
            missing_features = self.check_for_updates()  # Artık ana thread'de çağrılıyor
            self.downloader = FeatureDownloader(missing_features)
            self.downloader.progress.connect(self.ui.progressBox.append)
            self.downloader.start()
            logging.info("Feature download thread started.")
        except Exception as e:
            logging.error(f"Error starting feature download thread: {str(e)}")