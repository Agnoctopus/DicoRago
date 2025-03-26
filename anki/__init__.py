from aqt import mw
from aqt.qt import QAction, QMessageBox
import requests
import json
import os
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

# Base URL for your FastAPI backend
BASE_URL = "https://dicorago.com/api"

# Global variable to store the authentication token
auth_token = None

class AuthHandler(QObject):
    """
    Object exposed to the JavaScript context via QWebChannel.
    It allows the local page to send the authentication token to Python.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def sendToken(self, token: str):
        # Call parent's method to handle the received token.
        if self.parent() is not None:
            self.parent().on_token_received(token)

class LocalLoginDialog(QDialog):
    """
    A QDialog that embeds a QWebEngineView to display a local Vue.js login page.
    The page is responsible for handling offline notifications and triggering the
    online sign-in flow. Once the authentication is completed, it sends the token
    via QWebChannel.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dicorago Login")
        self.resize(800, 600)
        self.token = None

        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)

        # Set up QWebChannel for communication between JS and Python.
        self.channel = QWebChannel(self.web_view.page())
        self.auth_handler = AuthHandler(parent=self)
        self.channel.registerObject("authHandler", self.auth_handler)
        self.web_view.page().setWebChannel(self.channel)

        # Load the local HTML file (make sure it's in the same folder as __init__.py)
        local_html_path = os.path.join(os.path.dirname(__file__), "local_login.html")
        self.web_view.setUrl(QUrl.fromLocalFile(local_html_path))

    def on_token_received(self, token: str):
        """
        Called by the AuthHandler when the token is received from JavaScript.
        """
        self.token = token
        self.accept()  # Close the dialog indicating a successful login.

def user_login_via_local_page():
    """
    Opens the local login dialog (with Vue.js interface) for authentication.
    Returns the access token retrieved from the backend, or None if login fails.
    """
    global auth_token

    dialog = LocalLoginDialog(parent=mw)
    if dialog.exec():
        token = dialog.token
        if token:
            auth_token = token
            QMessageBox.information(mw, "Login", "Login successful!")
            return token
    QMessageBox.warning(mw, "Login", "Login failed or was cancelled.")
    return None

def sync_vocabulary():
    """
    Synchronizes the user's vocabulary with the backend.
    If the user is not logged in, it uses the local login page for authentication.
    Once authenticated, it calls the /sync-vocab route to fetch the vocabulary.
    """
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

# Create an action in the Tools menu to trigger vocabulary synchronization
action = QAction("Dicorago Sync", mw)
action.triggered.connect(sync_vocabulary)
mw.form.menuTools.addAction(action)
