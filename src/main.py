"""
Package: Jaal
Version: 1.0.0
Description: Jaal is a lightweight and privacy-focused web browser.
Author: Md. Ashraful Alam Shemul
Author GitHub: https://github.com/AAShemul
Developer: S Technologies
Developer URI: https://www.stechbd.net
GitHub Repository: https://github.com/STechBD/Jaal
Homepage: https://www.stechbd.net/product/Jaal
Created: April 24, 2023
License: MIT
License URI: https://opensource.org/licenses/MIT
"""

import sys
from urllib.parse import urlparse

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QTabWidget, QMessageBox, QToolBar

from bookmark_dialog import BookmarkDialog
from lib.bookmark import Bookmark


class Jaal(QMainWindow):
    """
    The main class of the Jaal Browser.

    :return: None
    :since: 1.0.0
    """
    remove_bookmark_signal = pyqtSignal(str)

    def __init__(self):
        """
        Constructor function to initialize the Jaal Browser.

        :return: None
        :since: 1.0.0
        """
        super().__init__()

        self.tab = None
        self.url_input = QLineEdit()
        self.setWindowTitle('Jaal Browser')
        self.setWindowIcon(QIcon('image/Jaal-Logo.webp'))
        self.bookmark_manager = Bookmark()
        self.remove_bookmark_signal.connect(self.remove_bookmark_by_url)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Menu Bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        self.edit_menu = self.menu_bar.addMenu('Edit')
        self.view_menu = self.menu_bar.addMenu('View')
        self.help_menu = self.menu_bar.addMenu('Help')

        # File Menu
        self.new_tab_action = QAction('New Tab', self)
        self.new_tab_action.triggered.connect(self.create_tab)
        self.file_menu.addAction(self.new_tab_action)

        self.bookmarks_action = QAction('Bookmarks', self)
        self.bookmarks_action.triggered.connect(self.show_bookmarks)
        self.file_menu.addAction(self.bookmarks_action)

        self.history_action = QAction('History', self)
        self.history_action.triggered.connect(self.show_history)
        self.file_menu.addAction(self.history_action)

        self.settings_action = QAction('Settings', self)
        self.settings_action.triggered.connect(self.show_settings)
        self.file_menu.addAction(self.settings_action)

        self.exit_action = QAction('Exit', self)
        self.exit_action.triggered.connect(exit_browser)
        self.file_menu.addAction(self.exit_action)

        # Edit Menu
        self.add_bookmark_action = QAction('Add Bookmark', self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.edit_menu.addAction(self.add_bookmark_action)

        self.remove_bookmark_action = QAction('Remove Bookmark', self)
        self.remove_bookmark_action.triggered.connect(self.remove_bookmark)
        self.edit_menu.addAction(self.remove_bookmark_action)

        # View Menu
        self.toggle_toolbar_action = QAction('Toggle Toolbar', self)
        self.toggle_toolbar_action.triggered.connect(self.toggle_toolbar)
        self.view_menu.addAction(self.toggle_toolbar_action)

        self.back_action = QAction('Back', self)
        self.back_action.triggered.connect(self.back)
        self.view_menu.addAction(self.back_action)

        self.forward_action = QAction('Forward', self)
        self.forward_action.triggered.connect(self.forward)
        self.view_menu.addAction(self.forward_action)

        self.reload_action = QAction('Reload', self)
        self.reload_action.triggered.connect(self.reload)
        self.view_menu.addAction(self.reload_action)

        self.stop_action = QAction('Stop', self)
        # UC # self.stop_action.triggered.connect(self.stop)
        self.view_menu.addAction(self.stop_action)

        # Help Menu
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Welcome')

        # Tool Bar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.back_button = QAction(QIcon('icon/back.svg'), 'Back', self)
        self.back_button.triggered.connect(self.back)
        self.toolbar.addAction(self.back_button)

        self.forward_button = QAction(QIcon('icon/forward.svg'), 'Forward', self)
        self.forward_button.triggered.connect(self.forward)
        self.toolbar.addAction(self.forward_button)

        self.reload_button = QAction(QIcon('icon/reload.svg'), 'Reload', self)
        self.reload_button.triggered.connect(self.reload)
        self.toolbar.addAction(self.reload_button)

        self.home_button = QAction(QIcon('icon/home.svg'), 'Home', self)
        self.home_button.triggered.connect(self.go_home)
        self.toolbar.addAction(self.home_button)

        self.url_input = QLineEdit(self)
        self.url_input.returnPressed.connect(lambda: self.load_url())
        self.toolbar.addWidget(self.url_input)

        self.toolbar.addSeparator()

        # Bookmark Widget
        self.add_bookmark_action = QAction(QIcon('icon/add-bookmark.svg'), 'Add Bookmark', self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.toolbar.addAction(self.add_bookmark_action)

        self.remove_bookmark_action = QAction(QIcon('icon/remove-bookmark.svg'), 'Remove Bookmark', self)
        self.remove_bookmark_action.triggered.connect(self.remove_bookmark)
        self.toolbar.addAction(self.remove_bookmark_action)

        # Check if the URL is bookmarked
        if self.tab:
            url = self.tab.url().toString()
            if self.bookmark_manager.is_bookmarked(url):
                self.add_bookmark_action.setEnabled(False)
                self.remove_bookmark_action.setEnabled(True)
            else:
                self.add_bookmark_action.setEnabled(True)
                self.remove_bookmark_action.setEnabled(False)

        # History List
        self.history_list = []
        self.create_tab()
        self.show()

    def create_tab(self):
        """
        Function to create a new tab.

        :return: None
        :since: 1.0.0
        """
        self.tab = QWebEngineView()
        self.tab.load(QUrl('https://www.stechbd.net'))
        self.tab.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(self.tab), title))
        self.tab.loadStarted.connect(self.tab_load_started)
        self.tab.loadFinished.connect(self.tab_load_finished)
        self.tabs.addTab(self.tab, 'New Tab')

    def tab_load_started(self):
        """
        Function to show a message in the status bar when a tab is loading.

        :return: None
        :since: 1.0.0
        """
        self.status_bar.showMessage('Loading ...')

    def tab_load_finished(self):
        """
        Function to show a message in the status bar when a tab is loaded.

        :return: None
        :since: 1.0.0
        """
        self.status_bar.showMessage('Page is Ready')

        # Add favicon to the tab
        url = self.tab.url().toString()
        if url.endswith('.ulkaa.com'):
            self.tabs.setTabIcon(self.tabs.indexOf(self.tab), QIcon('image/Ulkaa-Logo.webp'))
        else:
            self.tabs.setTabIcon(self.tabs.indexOf(self.tab), self.tab.icon())

        # Update the Address Bar
        self.url_input.setText(url)

        # Add the Current URL to the History
        url = self.tab.url().toString()
        if url not in self.history_list:
            self.history_list.append(url)

    def add_bookmark(self):
        """
        Function to add a bookmark.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            url = self.tab.url().toString()
            title = self.tab.title()
            self.bookmark_manager.add_bookmark(url, title)
            QMessageBox.information(self, 'Add Bookmark', 'Bookmark added successfully.')

    def remove_bookmark(self):
        """
        Function to remove a bookmark.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            url = self.tab.url().toString()
            self.bookmark_manager.remove_bookmark(url)
            QMessageBox.information(self, 'Remove Bookmark', 'Bookmark removed successfully.')

    def show_bookmarks(self):
        """
        Function to show bookmarks.

        :return: None
        :since: 1.0.0
        """
        bookmark_list = self.bookmark_manager.bookmarks
        if not bookmark_list:
            QMessageBox.information(self, 'Bookmarks', 'No bookmarks found.')
        else:
            dialog = BookmarkDialog(bookmark_list)
            dialog.open_url_signal.connect(self.load_url_in_current_tab)
            dialog.remove_bookmark_signal.connect(self.remove_bookmark_by_url)
            dialog.exec()

    def load_url_in_current_tab(self, url):
        """
        Function to load the URL in the current tab.

        :param url: The URL to be loaded.
        :return: None
        :since: 1.0.0
        """
        self.tab.load(QUrl(url))

    def remove_bookmark_by_url(self, url):
        """
        Function to remove a bookmark by URL.

        :param url: The URL of the bookmark to be removed.
        :return: None
        :since: 1.0.0
        """
        self.bookmark_manager.remove_bookmark(url)
        QMessageBox.information(self, 'Remove Bookmark', 'Bookmark removed successfully.')

    def show_settings(self):
        """
        Function to show settings.

        :return: None
        :since: 1.0.0
        """
        # Display the Bookmark List in a Message Box
        message_box = QMessageBox()
        # UC # message_box.setText("\n".join(self.bookmark_list))
        message_box.exec()

    def show_history(self):
        """
        Function to show history.

        :return: None
        :since: 1.0.0
        """
        # Display the History List in a Message Box
        message_box = QMessageBox()
        message_box.setText("\n".join(self.history_list))
        message_box.exec()

    def close_tab(self, index):
        """
        Function to close a tab.

        :param index: The index of the tab to be closed.
        :return: None
        :since: 1.0.0
        """
        self.tabs.removeTab(index)

        # If there is no tab left, create a new one
        if self.tabs.count() == 0:
            self.create_tab()

    def about(self):
        """
        Function to show the About dialog.

        :return: None
        :since: 1.0.0
        """
        QMessageBox.about(self, 'About Jaal Browser', 'Jaal is a desktop app for browsing websites.')

    def back(self):
        """
        Function to go back to the previous page.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            self.tab.back()

    def forward(self):
        """
        Function to go forward to the next page.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            self.tab.forward()

    def reload(self):
        """
        Function to reload the current page.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            self.tab.reload()

    def go_home(self):
        """
        Function to go to the home page.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            self.tab.load(QUrl('https://www.stechbd.net'))

    def load_url(self):
        """
        Function to load the URL in the address bar.

        :return: None
        :since: 1.0.0
        """
        url = self.url_input.text().strip()
        if url:
            if not urlparse(url).scheme:
                url = 'https://' + url

        self.tab.load(QUrl(url))

    def toggle_toolbar(self, checked):
        """
        Function to toggle the toolbar.

        :param checked: The state of the toolbar.
        :return: None
        :since: 1.0.0
        """
        if checked:
            self.toolbar.show()
        else:
            self.toolbar.hide()


def exit_browser():
    """
    Function to exit the browser.

    :return: None
    :since: 1.0.0
    """
    sys.exit()


"""
The main function to run the Jaal Browser.

:return: None
:since: 1.0.0
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Jaal()
    app.exec()
