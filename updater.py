import sys
import os
import requests
import zipfile
import shutil
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

VERSION_URL = "https://uurwares.s3.eu-north-1.amazonaws.com/version.json"
ZIP_URL = "https://uurwares.s3.eu-north-1.amazonaws.com/UurWares.zip"
LOCAL_VERSION_FILE = os.path.join(os.getcwd(), "version.json")
DOWNLOAD_PATH = resource_path("UurWares.zip")

class UpdaterThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def run(self):
        try:
            self.status.emit("Uzak sürüm kontrol ediliyor...")
            remote_version = requests.get(VERSION_URL).json()["client"]["version"]
            if os.path.exists(LOCAL_VERSION_FILE):
                with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
                    local_version = json.load(f)["client"]["version"]
            else:
                local_version = None
            if local_version == remote_version:
                self.status.emit("Güncel sürüm zaten yüklü.")
                self.finished.emit(True)
                return
            self.status.emit("Güncelleme indiriliyor...")
            with requests.get(ZIP_URL, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                with open(DOWNLOAD_PATH, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int(downloaded * 100 / total) if total else 0
                            self.progress.emit(percent)
            self.status.emit("Zip dosyası çıkartılıyor...")
            with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
                extract_path = os.path.abspath(".")
                for member in zip_ref.namelist():
                    self.status.emit(f"Çıkartılıyor: {member}")
                    zip_ref.extract(member, extract_path)
            # Zip dosyasını sil
            if os.path.exists(DOWNLOAD_PATH):
                os.remove(DOWNLOAD_PATH)
            self.status.emit("Güncelleme tamamlandı.")
            self.finished.emit(True)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.status.emit(f"Hata: {e}\n{tb}")
            self.finished.emit(False)

class UpdaterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UurWares Güncelleyici")
        self.setGeometry(600, 300, 400, 200)
        layout = QVBoxLayout()
        self.label = QLabel("Güncelleme durumu bekleniyor...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("Güncellemeyi Başlat")
        self.button.clicked.connect(self.start_update)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.updater_thread = None

    def start_update(self):
        self.button.setEnabled(False)
        self.updater_thread = UpdaterThread()
        self.updater_thread.progress.connect(self.progress.setValue)
        self.updater_thread.status.connect(self.label.setText)
        self.updater_thread.finished.connect(self.on_finish)
        self.updater_thread.start()

    def on_finish(self, success):
        self.button.setEnabled(True)
        if success:
            if self.label.text() == "Güncel sürüm zaten yüklü.":
                self.progress.setValue(0)
                self.label.setText("Zaten en güncel sürüm yüklü.")
            else:
                self.label.setText("Güncelleme tamamlandı!")
        else:
            self.label.setText("Güncelleme başarısız oldu.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdaterGUI()
    window.show()
    sys.exit(app.exec())