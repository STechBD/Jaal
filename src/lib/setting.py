import os
import sqlite3
from datetime import datetime


class Setting:
    def __init__(self):
        # Use absolute path for database file
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '..', 'data', 'bookmark.db')
        self.init_db()

        self.default_setting = {
            'homepage': 'jaal://home',
            'search_engine': 'google',
            'mode': 'light',
            'download_dir': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'user': None
        }

    def init_db(self):
        # Ensure directory exists before connecting
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setting (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def set_setting(self, name, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO setting (name, value) VALUES (?, ?)', (name, value))
        conn.commit()
        conn.close()

    def get_setting(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM setting WHERE name = ?', (name,))
        setting = cursor.fetchone()
        conn.close()
        return setting[0] if setting else None

    def update_setting(self, name, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE setting SET value = ? WHERE name = ?', (value, name))
        conn.commit()
        conn.close()

    def delete_setting(self, name):
        get_default_setting = self.default_setting.get(name)
        self.update_setting(name, get_default_setting)

    def get_all_setting(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, value FROM setting')
        setting = cursor.fetchall()
        conn.close()
        return setting

    def remove_all_setting(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM setting')
        conn.commit()
        conn.close()

    def is_setting(self, name) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM setting WHERE name = ?', (name,))
        setting = cursor.fetchone()
        return setting is not None

    def set_default_setting(self):
        for name, value in self.default_setting.items():
            if not self.is_setting(name):
                self.set_setting(name, value)
            else:
                self.update_setting(name, value)
