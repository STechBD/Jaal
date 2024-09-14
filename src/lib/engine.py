from PyQt6.QtWebEngineCore import QWebEnginePage


class JaalEngine(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_agent = 'Jaal Browser/1.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def createRequest(self, request, nav_type, form_data):
        request.setRawHeader(b'User-Agent', self.user_agent.encode())
        return super().createRequest(request, nav_type, form_data)
