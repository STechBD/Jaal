from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal


class BookmarkDialog(QDialog):
    open_url_signal = pyqtSignal(str)
    remove_bookmark_signal = pyqtSignal(str)

    def __init__(self, bookmarks):
        super().__init__()
        self.setWindowTitle('Bookmarks')
        self.setLayout(QVBoxLayout())

        for bookmark in bookmarks:
            title = bookmark['title']
            url = bookmark['url']
            self.add_bookmark_item(title, url)

    def add_bookmark_item(self, title, url):
        layout = QHBoxLayout()

        link = QLabel(f'<a href="{url}">{title}</a>')
        link.setOpenExternalLinks(False)
        link.linkActivated.connect(self.open_url)

        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(lambda: self.remove_bookmark(url))

        layout.addWidget(link)
        layout.addWidget(remove_button)

        self.layout().addLayout(layout)

    def open_url(self, url):
        self.open_url_signal.emit(url)
        self.accept()

    def remove_bookmark(self, url):
        self.remove_bookmark_signal.emit(url)
