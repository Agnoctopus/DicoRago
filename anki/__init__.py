from aqt import mw
from aqt.qt import QAction, QMessageBox
import requests
import os
import json
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEnginePage

BASE_URL = "https://dicorago.com/api"

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Print JS console messages to Python's console for debugging.
        print(f"JS Console: {message}")
        print(f"(Source: {sourceID}, Line: {lineNumber})")

class AnkiBridge(QObject):
    @pyqtSlot(str)
    def syncVocabulary(self, vocab_json: str):
        """
        This slot receives a JSON string containing a list of words (their 'written' property)
        and sends it to the synchronization API.
        """
        try:
            vocab_list = json.loads(vocab_json)
        except Exception as e:
            QMessageBox.critical(mw, "Dicorago Sync", f"Error parsing vocabulary data: {str(e)}")
            return

        try:
            response = requests.post(f"{BASE_URL}/sync-vocab", json={"vocab": vocab_list})
            if response.status_code == 200:
                QMessageBox.information(mw, "Dicorago Sync", "Vocabulary synced successfully!")
            else:
                QMessageBox.warning(mw, "Dicorago Sync", f"Error syncing vocabulary: {response.text}")
        except Exception as e:
            QMessageBox.critical(mw, "Dicorago Sync", f"An error occurred: {str(e)}")

class VocabSyncDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sync Vocabulary")
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        # Create a QWebEngineView with a custom page that prints JS console messages.
        self.web_view = QWebEngineView(self)
        custom_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(custom_page)
        layout.addWidget(self.web_view)

        # Initialize QWebChannel for communication with the Vue page.
        self.channel = QWebChannel(self.web_view.page())
        self.anki_bridge = AnkiBridge(parent=self)
        self.channel.registerObject("anki", self.anki_bridge)
        print("Anki bridge registered")
        self.web_view.page().setWebChannel(self.channel)

        # Load the local sync page (index.html from your Vue build).
        local_html_path = os.path.join(os.path.dirname(__file__), "dicorago-anki", "dist", "index.html")
        print("Loading sync page:", local_html_path)
        self.web_view.setUrl(QUrl.fromLocalFile(local_html_path))

def sync_vocabulary():
    """
    Opens a dialog that displays the Vue-based sync interface.
    """
    dialog = VocabSyncDialog(parent=mw)
    dialog.exec()

# Add the "Dicorago Sync" action to Anki's Tools menu.
action = QAction("Dicorago Sync", mw)
action.triggered.connect(sync_vocabulary)
mw.form.menuTools.addAction(action)
