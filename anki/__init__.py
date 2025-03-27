from aqt import mw
from aqt.qt import QAction, QMessageBox
import requests
import os
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

BASE_URL = "https://dicorago.com/api"
auth_token = None

class AuthHandler(QObject):
    @pyqtSlot(str)
    def sendToken(self, token: str):
        if self.parent():
            self.parent().on_token_received(token)

class LocalLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dicorago Login")
        self.resize(800, 600)
        self.token = None
        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)
        self.channel = QWebChannel(self.web_view.page())
        self.auth_handler = AuthHandler(parent=self)
        self.channel.registerObject("authHandler", self.auth_handler)
        self.web_view.page().setWebChannel(self.channel)
        local_html_path = os.path.join(os.path.dirname(__file__), "dicorago-anki/dist", "index.html")
        print(local_html_path)
        self.web_view.setUrl(QUrl.fromLocalFile(local_html_path))
    def on_token_received(self, token: str):
        self.token = token
        self.accept()

def user_login_via_local_page():
    global auth_token
    print(1)
    dialog = LocalLoginDialog(parent=mw)
    print(2)

    if dialog.exec():
        print(3)

        token = dialog.token
        if token:
            auth_token = token
            QMessageBox.information(mw, "Login", "Login successful!")
            return token
    QMessageBox.warning(mw, "Login", "Login failed or was cancelled.")
    return None

def sync_vocabulary():
    global auth_token
    if not auth_token:
        token = user_login_via_local_page()
        if not token:
            return
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{BASE_URL}/sync-vocab", headers=headers)
        if response.status_code == 200:
            vocab_data = response.json()
            keys = list(vocab_data.keys())
            QMessageBox.information(mw, "Dicorago Sync", f"Vocabulary synchronized:\n{keys}")
        else:
            QMessageBox.warning(mw, "Dicorago Sync", f"Failed to sync vocabulary: {response.text}")
    except Exception as e:
        QMessageBox.critical(mw, "Sync Error", f"An error occurred: {str(e)}")

action = QAction("Dicorago Sync", mw)
action.triggered.connect(sync_vocabulary)
mw.form.menuTools.addAction(action)
