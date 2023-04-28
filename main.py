"""
Package: PyWeb
Version: 1.0.0
Description: PyWeb is a web browser made with Python and PyQt6.
Author: Md. Ashraful Alam Shemul
Author URI: https://www.aashemul.com
Author GitHub: https://github.com/AAShemul
GitHub Repository: https://github.com/AAShemul/PyWeb
Created: April 24, 2023
Updated: April 26, 2023
License: MIT
License URI: https://opensource.org/licenses/MIT
"""

import sys
from urllib.parse import urlparse
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QTabWidget, QMenu, \
	QMenuBar, QStatusBar, QMessageBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl


class PyWeb:
	def __init__(self):
		super().__init__()

		self.tab = None
		self.setWindowTitle('PyWeb Browser')
		self.setWindowIcon(QIcon('image/PyWeb-Logo.webp'))

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

		# Help Menu
		self.about_action = QAction('About', self)
		self.about_action.triggered.connect(self.show_about)
		self.help_menu.addAction(self.about_action)

		self.about_qt_action = QAction('About Qt', self)
		self.about_qt_action.triggered.connect(self.show_about_qt)
		self.help_menu.addAction(self.about_qt_action)

		# Tool Bar
		self.tool_bar = QToolBar()
		self.addToolBar(self.tool_bar)

		self.back_action = QAction(QIcon('image/back.png'), 'Back', self)
		self.back_action.triggered.connect(self.back)
		self.tool_bar.addAction(self.back_action)

		self.forward_action = QAction(QIcon('image/forward.png'), 'Forward', self)
		self.forward_action.triggered.connect(self.forward)
		self.tool_bar.addAction(self.forward_action)

		self.reload_action = QAction(QIcon('image/reload.png'), 'Reload', self)
		self.reload_action.triggered.connect(self.reload)
		self.tool_bar.addAction(self.reload_action)

		self.stop_action = QAction(QIcon('image/stop.png'), 'Stop', self)
		self.stop_action.triggered.connect(self.stop)
		self.tool_bar.addAction(self.stop_action)

		self.tool_bar.addSeparator()

		self.home_action = QAction(QIcon('image/home.png'), 'Home', self)
		self.home_action.triggered.connect(self.home)
		self.tool_bar.addAction(self.home_action)

		self.tool_bar.addSeparator()

		self.add_bookmark_action = QAction(QIcon('image/add-bookmark.png'), 'Add Bookmark', self)
		self.add_bookmark_action.triggered.connect(self.add_bookmark)
		self.tool_bar.addAction(self.add_bookmark_action)

		self.remove_bookmark_action = QAction(QIcon('image/remove-bookmark.png'), 'Remove Bookmark', self)
		self.remove_bookmark_action.triggered.connect(self.remove_bookmark)
		self.tool_bar.addAction(self.remove_bookmark_action)

		# Tab Widget
		self.tabs = QTabWidget()
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_tab)
		self.setCentralWidget(self.tabs)

		# History List
		self.history_list = []
		self.create_tab()
		self.show()

	# Create Tab
	def create_tab(self):
		self.tab = QWebEngineView
		self.tab.setUrl(QUrl('https://www.stechbd.net'))
		self.tab.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(self.tab), title))
		self.tab.urlChanged.connect(self.update_urlbar)
		self.tab.loadFinished.connect(self.update_title)
		self.tabs.addTab(self.tab, 'New Tab')
		self.tabs.setCurrentWidget(self.tab)

	def tab_load_started(self):
		self.status_bar.showMessage('Loading ...')

	def tab_load_finished(self):
		self.status_bar.showMessage('Page loaded')

		# Add Favicon
		# Add Current URL to the History
		url = self.tab.url().toString()
		if url not in self.history_list:
			self.history_list.append(url)

		# Update the Address Bar
		self.url_input.setText(url)


if __name__ == '__main__':
	app = QApplication([])
	window = PyWeb()
	app.exec()
