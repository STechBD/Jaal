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
import os
import threading
import ctypes
from datetime import datetime
from urllib.parse import urlparse

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTabWidget, QMessageBox, QToolBar


import qdarktheme

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import app as flask_app
from lib.engine import JaalEngine
from lib.setting import Setting
from lib.bookmark import Bookmark
from lib.history import History


class Jaal(QMainWindow):
    """
    The main class of the Jaal Browser.

    :return: None
    :since: 1.0.0
    """

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
        self.setWindowIcon(QIcon('image/Jaal-Logo-Round.svg'))
        self.setting_manager = Setting()
        self.bookmark_manager = Bookmark()
        self.history_manager = History()
        self.dark_mode = self.setting_manager.get_setting('mode') == 'dark'

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.update_url_input)

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
        self.bookmarks_action.triggered.connect(self.show_bookmark_manager)
        self.bookmarks_action.setShortcut('Ctrl+B')
        self.file_menu.addAction(self.bookmarks_action)

        self.history_action = QAction('History', self)
        self.history_action.triggered.connect(self.show_history)
        self.history_action.setShortcut('Ctrl+H')
        self.file_menu.addAction(self.history_action)

        self.settings_action = QAction('Settings', self)
        self.settings_action.triggered.connect(self.show_settings)
        self.settings_action.setShortcut('Ctrl+,')
        self.file_menu.addAction(self.settings_action)

        self.exit_action = QAction('Exit', self)
        self.exit_action.triggered.connect(self.exit_browser)
        self.exit_action.setShortcut('Ctrl+Q')
        self.file_menu.addAction(self.exit_action)

        self.mode_action = QAction('Dark Mode', self)
        self.mode_action.triggered.connect(self.mode)
        self.mode_action.setShortcut('Ctrl+M')
        self.file_menu.addAction(self.mode_action)

        # Edit Menu
        self.add_bookmark_action = QAction('Add Bookmark', self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.add_bookmark_action.setShortcut('Ctrl+D')
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
        self.stop_action.triggered.connect(self.stop)
        self.view_menu.addAction(self.stop_action)

        self.stop_action = QAction('Stop', self)
        self.stop_action.triggered.connect(self.stop)
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

        self.back_button = QAction(QIcon('image/back.svg'), 'Back', self)
        self.back_button.triggered.connect(self.back)
        self.back_button.setShortcut('Alt+Left')
        self.toolbar.addAction(self.back_button)

        self.forward_button = QAction(QIcon('image/forward.svg'), 'Forward', self)
        self.forward_button.triggered.connect(self.forward)
        self.toolbar.addAction(self.forward_button)

        self.reload_button = QAction(QIcon('image/reload.svg'), 'Reload', self)
        self.reload_button.triggered.connect(self.reload)
        self.reload_button.setShortcut('Ctrl+R')
        self.reload_button.setShortcut('F5')
        self.toolbar.addAction(self.reload_button)

        self.stop_button = QAction(QIcon('image/stop.svg'), 'Stop', self)
        self.stop_button.triggered.connect(self.stop)
        self.stop_button.setShortcut('Esc')
        self.toolbar.addAction(self.stop_button)

        self.home_button = QAction(QIcon('image/home.svg'), 'Home', self)
        self.home_button.triggered.connect(self.go_home)
        self.toolbar.addAction(self.home_button)

        self.url_input = QLineEdit(self)
        self.url_input.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_input)

        self.toolbar.addSeparator()

        # New Tab Button
        self.new_tab_button = QAction(QIcon('image/new.svg'), 'New Tab', self)
        self.new_tab_button.triggered.connect(self.create_tab)
        self.new_tab_button.setShortcut('Ctrl+T')
        self.toolbar.addAction(self.new_tab_button)

        # Bookmark Widget
        self.add_bookmark_action = QAction(QIcon('image/add-bookmark.svg'), 'Add Bookmark', self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.toolbar.addAction(self.add_bookmark_action)

        self.remove_bookmark_action = QAction(QIcon('image/remove-bookmark.svg'), 'Remove Bookmark', self)
        self.remove_bookmark_action.triggered.connect(self.remove_bookmark)
        self.toolbar.addAction(self.remove_bookmark_action)

        # Start the Flask server in a separate thread
        self.start_flask_server()

        # Start the browser
        self.create_tab()
        self.showMaximized()

    def create_tab(self, url='jaal://home'):
        self.tab = QWebEngineView()
        page = JaalEngine(self.tab)
        page.createWindow = self.handle_create_new_tab
        self.tab.setPage(page)

        if not isinstance(url, str):
            url = 'jaal://home'

        if url.startswith('jaal://'):
            url = self.handle_jaal_url(url)

        self.tab.load(QUrl(url))
        self.tab.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(self.tab), title))
        self.tab.loadStarted.connect(self.tab_load_started)
        self.tab.loadFinished.connect(self.tab_load_finished)
        self.tabs.addTab(self.tab, 'New Tab')
        self.tabs.setCurrentWidget(self.tab)

    def update_url_input(self, index):
        """
        Function to update the URL input box when the tab changes.

        :param index: Index of the current tab.
        :return: None
        :since: 1.0.0
        """
        current_tab = self.tabs.widget(index)
        if current_tab:
            url = current_tab.url().toString()
            if url.startswith('http://localhost:5000/'):
                url = url.replace('http://localhost:5000/', 'jaal://')
            self.url_input.setText(url)

    def handle_create_new_tab(self, _):
        new_tab = QWebEngineView()
        new_tab.setPage(JaalEngine(new_tab))

        # Create a new tab for the request
        self.tabs.addTab(new_tab, 'New Tab')
        self.tabs.setCurrentWidget(new_tab)

        # Update the Address Bar
        url = new_tab.url().toString()
        if url.startswith('http://localhost:5000/'):
            url = url.replace('http://localhost:5000/', 'jaal://')
        self.url_input.setText(url)

        new_tab.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(new_tab), title))
        new_tab.loadStarted.connect(self.tab_load_started)
        new_tab.loadFinished.connect(self.tab_load_finished)

        return new_tab.page()

    @staticmethod
    def handle_jaal_url(url):
        if url == 'jaal://home':
            return 'http://localhost:5000/'
        elif url == 'jaal://about':
            return 'http://localhost:5000/about'
        elif url == 'jaal://bookmark':
            return 'http://localhost:5000/bookmark'
        elif url == 'jaal://get_bookmark':
            return 'http://localhost:5000/get_bookmark'
        elif url == 'jaal://add_bookmark':
            return 'http://localhost:5000/add_bookmark'
        elif url == 'jaal://remove_bookmark':
            return 'http://localhost:5000/remove_bookmark'
        elif url == 'jaal://history':
            return 'http://localhost:5000/history'
        elif url == 'jaal://get_history':
            return 'http://localhost:5000/get_history'
        elif url == 'jaal://add_history':
            return 'http://localhost:5000/add_history'
        elif url == 'jaal://remove_history':
            return 'http://localhost:5000/remove_history'
        elif url == 'jaal://setting':
            return 'http://localhost:5000/setting'
        else:
            return 'http://localhost:5000/'

    def show_bookmark_manager(self):
        self.create_tab(url='jaal://bookmark')

    def tab_load_started(self):
        """
        Function to show a message in the status bar when a tab is loading.

        :return: None
        :since: 1.0.0
        """
        self.status_bar.showMessage('Loading ...')
        self.reload_button.setVisible(False)
        self.stop_button.setVisible(True)

    def tab_load_finished(self):
        """
        Function to show a message in the status bar when a tab is loaded.

        :return: None
        :since: 1.0.0
        """
        self.status_bar.showMessage('Page is Ready')
        self.reload_button.setVisible(True)
        self.stop_button.setVisible(False)

        # Add favicon to the tab
        url = self.tab.url().toString()
        domain = urlparse(url).netloc
        self.tabs.setTabIcon(self.tabs.indexOf(self.tab), self.tab.icon())

        # Update the Address Bar
        if url.startswith('http://localhost:5000/'):
            url = url.replace('http://localhost:5000/', 'jaal://')
        self.url_input.setText(url)

        # Add the Current URL to the History
        if not url.startswith('jaal://') and not url.startswith('http://localhost:5000/'):
            icon_path = self.tab.icon().pixmap(16, 16).toImage().save(domain + '.ico', 'ICO')
            self.add_history_entry(self.tab.title(), url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), icon_path)

        # Update bookmark actions based on whether the URL is bookmarked
        if self.bookmark_manager.is_bookmarked(url):
            self.add_bookmark_action.setVisible(False)
            self.remove_bookmark_action.setVisible(True)
        else:
            self.add_bookmark_action.setVisible(True)
            self.remove_bookmark_action.setVisible(False)

    def add_bookmark(self):
        """
        Function to add a bookmark.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            url = self.tab.url().toString()
            title = self.tab.title()

            if not self.bookmark_manager.is_bookmarked(url):
                self.bookmark_manager.add_bookmark(title, url, favicon=self.tab.icon().pixmap(16, 16).toImage().save(url + '.ico', 'ICO'))
                QMessageBox.information(self, 'Add Bookmark', 'Bookmark added successfully.')
                self.add_bookmark_action.setVisible(False)
                self.remove_bookmark_action.setVisible(True)
            else:
                QMessageBox.information(self, 'Add Bookmark', 'Bookmark already exists.')

    def remove_bookmark(self):
        """
        Function to remove a bookmark.

        :return: None
        :since: 1.0.0
        """
        if self.tab:
            url = self.tab.url().toString()
            self.bookmark_manager.remove_bookmark(url)

            if self.bookmark_manager.is_bookmarked(url):
                QMessageBox.information(self, 'Remove Bookmark', 'Bookmark removed successfully.')
                self.add_bookmark_action.setVisible(True)
                self.remove_bookmark_action.setVisible(False)
            else:
                QMessageBox.information(self, 'Remove Bookmark', 'Bookmark does not exist.')

    def show_history(self):
        self.create_tab(url='jaal://history')

    def add_history_entry(self, title, url, time, favicon):
        """
        Function to add a history entry.

        :param title: Title of the page.
        :param url: URL of the page.
        :param time: Time when the page was visited.
        :param favicon: Favicon of the page.
        :return: None
        """
        self.history_manager.add_history_entry(title, url, time, favicon)

    def remove_history_entry(self, history_id):
        """
        Function to remove a history entry.

        :param history_id: ID of the history entry to be removed.
        :return: None
        """
        self.history_manager.remove_history_entry(history_id)

    def show_settings(self):
        """
        Function to show the settings.

        :return: None
        :since: 1.0.0
        """
        self.create_tab(url='jaal://setting')

    def close_tab(self, index):
        """
        Function to close a tab.

        :param index: Index of the tab to be closed.
        :return: None
        :since: 1.0.0
        """
        self.tabs.removeTab(index)

        # Close the browser if there are no tabs left
        if self.tabs.count() == 0:
            self.exit_browser()

    def go_home(self):
        """
        Function to go to the home page.

        :return: None
        :since: 1.0.0
        """
        self.tab.setUrl(QUrl('https://www.stechbd.net'))

    def load_url(self):
        """
        Function to load the URL in the address bar.

        :return: None
        :since: 1.0.0
        """
        url = self.url_input.text()

        if url.startswith('jaal://'):
            url = self.handle_jaal_url(url)
        elif (' ' or '@') in url:
            url = 'https://www.google.com/search?q=' + '+'.join(url.split(' '))
        elif not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        self.tab.setUrl(QUrl(url))

    def back(self):
        """
        Function to navigate back.

        :return: None
        :since: 1.0.0
        """
        self.tab.back()

    def forward(self):
        """
        Function to navigate forward.

        :return: None
        :since: 1.0.0
        """
        self.tab.forward()

    def reload(self):
        """
        Function to reload the current page.

        :return: None
        :since: 1.0.0
        """
        self.tab.reload()

    def stop(self):
        """
        Function to stop loading the current page.

        :return: None
        :since: 1.0.0
        """
        self.tab.stop()

    def toggle_toolbar(self):
        """
        Function to toggle the visibility of the toolbar.

        :return: None
        :since: 1.0.0
        """
        self.toolbar.setVisible(not self.toolbar.isVisible())

    def about(self):
        """
        Function to show the about dialog.

        :return: None
        :since: 1.0.0
        """
        self.create_tab(url='jaal://about')

    @staticmethod
    def exit_browser():
        """
        Function to exit the browser.

        :return: None
        :since: 1.0.0
        """
        QApplication.quit()

    def mode(self):
        """
        Function to change the mode of the browser.

        :return: None
        :since: 1.0.0
        """
        self.dark_mode = not self.dark_mode
        self.apply_mode()

    def apply_mode(self):
        """
        Apply the current mode (dark or light).
        """
        if self.dark_mode:
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet('dark'))
            self.mode_action.setText('Light Mode')
            self.setting_manager.update_setting('mode', 'dark')
        else:
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet('light'))
            self.mode_action.setText('Dark Mode')
            self.setting_manager.update_setting('mode', 'light')

    @staticmethod
    def start_flask_server():
        """
        Function to start the Flask server in a separate thread.

        :return: None
        :since: 1.0.0
        """
        flask_thread = threading.Thread(target=flask_app.run)
        flask_thread.daemon = True
        flask_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the app user model ID for Windows
    if os.name == 'nt':  # Check if the OS is Windows
        myappid = 'net.stechbd.jaal'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app.setWindowIcon(QIcon('image/Jaal-Logo-Round.ico'))
    Jaal()

    sys.exit(app.exec())
