import os
import sqlite3


class History:
    def __init__(self):
        # Use absolute path for database file
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '..', 'data', 'history.db')
        self.init_db()

    def init_db(self):
        # Ensure directory exists before connecting
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                time TEXT,
                favicon BLOB
            )
        ''')
        conn.commit()
        conn.close()

    def add_history_entry(self, title, url, time, favicon):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (title, url, time, favicon) VALUES (?, ?, ?, ?)',
                       (title, url, time, favicon))
        conn.commit()
        conn.close()

    def is_in_history(self, url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM history WHERE url=?', (url,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def get_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, url, time, favicon FROM history ORDER BY id DESC')
        history_entries = cursor.fetchall()
        conn.close()
        return history_entries

    def remove_history_entry(self, history_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history WHERE id=?', (history_id,))
        conn.commit()
        conn.close()
