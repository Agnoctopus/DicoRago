from aqt import mw
from aqt.qt import QAction, QMessageBox
import requests
import os
import json
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

BASE_URL = "https://dicorago.com/api"

class AnkiBridge(QObject):
    @pyqtSlot(str)
    def syncVocabulary(self, vocab_json: str):
        """
        Ce slot reçoit une chaîne JSON contenant la liste des mots (propriété "written")
        et l'envoie à l'API de synchronisation.
        """
        try:
            # On s'attend à recevoir un JSON sous la forme d'une liste de chaînes.
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
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)

        # Initialisation du QWebChannel pour la communication avec la page Vue.
        self.channel = QWebChannel(self.web_view.page())
        self.anki_bridge = AnkiBridge(parent=self)
        self.channel.registerObject("anki", self.anki_bridge)
        self.web_view.page().setWebChannel(self.channel)

        # Chargez la page locale de synchronisation (sync.html issu de votre build Vue).
        local_html_path = os.path.join(os.path.dirname(__file__), "dicorago-anki", "dist", "index.html")
        print("Loading sync page:", local_html_path)
        self.web_view.setUrl(QUrl.fromLocalFile(local_html_path))

def sync_vocabulary():
    # Ouvre une boîte de dialogue affichant l'interface Vue de synchronisation.
    dialog = VocabSyncDialog(parent=mw)
    dialog.exec()

# Ajout de l'action dans le menu Outils d'Anki.
action = QAction("Dicorago Sync", mw)
action.triggered.connect(sync_vocabulary)
mw.form.menuTools.addAction(action)
