from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget
import os


class History(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath('tab/history.html')))

        layout.addWidget(self.web_view)
        self.setLayout(layout)
