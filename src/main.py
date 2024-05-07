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


class PyWeb(QMainWindow):
	def __init__(self):
		super().__init__()

		self.tab = None
		self.url_input = QLineEdit()
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
		self.tool_bar = QToolBar()
		self.addToolBar(self.tool_bar)

		self.back_button = QAction(QIcon('icon/back.svg'), 'Back', self)
		self.back_button.triggered.connect(self.back)
		self.tool_bar.addAction(self.back_button)

		self.forward_button = QAction(QIcon('icon/forward.svg'), 'Forward', self)
		self.forward_button.triggered.connect(self.forward)
		self.tool_bar.addAction(self.forward_button)

		self.reload_button = QAction(QIcon('icon/reload.svg'), 'Reload', self)
		self.reload_button.triggered.connect(self.reload)
		self.tool_bar.addAction(self.reload_button)

		self.stop_action = QAction(QIcon('image/stop.png'), 'Stop', self)
		# UC # self.stop_action.triggered.connect(self.stop)
		self.tool_bar.addAction(self.stop_action)

		self.home_button = QAction(QIcon('icon/home.svg'), 'Home', self)
		self.home_button.triggered.connect(self.go_home)
		self.tool_bar.addAction(self.home_button)

		self.url_input = QLineEdit(self)
		self.url_input.returnPressed.connect(lambda: self.load_url())
		self.tool_bar.addWidget(self.url_input)

		self.tool_bar.addSeparator()

		self.add_bookmark_action = QAction(QIcon('icon/add-bookmark.svg'), 'Add Bookmark', self)
		self.add_bookmark_action.triggered.connect(self.add_bookmark)
		self.tool_bar.addAction(self.add_bookmark_action)

		self.remove_bookmark_action = QAction(QIcon('icon/remove-bookmark.svg'), 'Remove Bookmark', self)
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
		self.tab = QWebEngineView()
		self.tab.load(QUrl('https://www.stechbd.net'))
		self.tab.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(self.tab), title))
		self.tab.loadStarted.connect(self.tab_load_started)
		self.tab.loadFinished.connect(self.tab_load_finished)
		self.tabs.setCurrentWidget(self.tab)

	def tab_load_started(self):
		self.status_bar.showMessage('Loading ...')

	def tab_load_finished(self):
		self.status_bar.showMessage('Page is ready')
		url = self.tab.url().toString()

		# UC # Add Favicon

		# Update the Address Bar
		self.url_input.setText(url)

		# Add Current URL to the History
		if url not in self.history_list:
			self.history_list.append(url)

	def add_bookmark(self):
		# Display the Bookmark List in a Message Box
		message_box = QMessageBox()
		# UC # message_box.setText("\n".join(self.bookmark_list))
		message_box.exec()

	def remove_bookmark(self):
		# Display the Bookmark List in a Message Box
		message_box = QMessageBox()
		# UC # message_box.setText("\n".join(self.bookmark_list))
		message_box.exec()

	def show_bookmarks(self):
		# Display the Bookmark List in a Message Box
		message_box = QMessageBox()
		# UC # message_box.setText("\n".join(self.bookmark_list))
		message_box.exec()

	def show_settings(self):
		# Display the Bookmark List in a Message Box
		message_box = QMessageBox()
		# UC # message_box.setText("\n".join(self.bookmark_list))
		message_box.exec()

	def show_history(self):
		# Display the History List in a Message Box
		message_box = QMessageBox()
		message_box.setText("\n".join(self.history_list))
		message_box.exec()

	def close_tab(self, index):
		self.tabs.removeTab(index)

		# If there is no tab left, create a new one
		if self.tabs.count() == 0:
			self.create_tab()

	def about(self):
		QMessageBox.about(self, 'About PyWeb Browser', 'PyWeb is a desktop app for browsing websites.')

	def back(self):
		if self.tab:
			self.tab.back()

	def forward(self):
		if self.tab:
			self.tab.forward()

	def reload(self):
		if self.tab:
			self.tab.reload()

	def go_home(self):
		if self.tab:
			self.tab.load(QUrl('https://www.stechbd.net'))

	def load_url(self):
		url = self.url_input.text().strip()
		if url:
			if not urlparse(url).scheme:
				url = 'https://' + url

		self.tab.load(QUrl(url))

	def toggle_toolbar(self, checked):
		if checked:
			self.tool_bar.show()
		else:
			self.tool_bar.hide()


def exit_browser():
	sys.exit()


if __name__ == '__main__':
	app = QApplication([])
	window = PyWeb()
	app.exec()
