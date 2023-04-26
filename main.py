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
	# Main class

if __name__ == '__main__':
	app = QApplication([])
	window = PyWeb()
	app.exec()
