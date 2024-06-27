import os
import sqlite3


class Bookmark:
    def __init__(self):
        # Use absolute path for database file
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '..', 'data', 'bookmark.db')
        self.init_db()

    def init_db(self):
        # Ensure directory exists before connecting
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmark (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                favicon BLOB,
                folder_id INTEGER,
                FOREIGN KEY (folder_id) REFERENCES folder(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folder (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES folder(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_bookmark(self, title, url, favicon=None, folder_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmark (title, url, favicon, folder_id) VALUES (?, ?, ?, ?)',
                       (title, url, favicon, folder_id))
        conn.commit()
        conn.close()

    def get_bookmark(self, folder_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if folder_id:
            cursor.execute('SELECT id, title, url, favicon, folder_id FROM bookmark WHERE folder_id = ?', (folder_id,))
        else:
            cursor.execute('SELECT id, title, url, favicon, folder_id FROM bookmark WHERE folder_id IS NULL')
        bookmark = cursor.fetchall()
        conn.close()
        return bookmark

    def remove_bookmark(self, bookmark_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookmark WHERE id = ?', (bookmark_id,))
        conn.commit()
        conn.close()

    def is_bookmarked(self, url) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM bookmark WHERE url = ?', (url,))
        bookmark = cursor.fetchone()
        conn.close()
        return bookmark is not None

    def add_folder(self, name, parent_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO folder (name, parent_id) VALUES (?, ?)', (name, parent_id))
        conn.commit()
        conn.close()

    def get_folder(self, parent_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if parent_id:
            cursor.execute('SELECT id, name, parent_id FROM folder WHERE parent_id = ?', (parent_id,))
        else:
            cursor.execute('SELECT id, name, parent_id FROM folder WHERE parent_id IS NULL')
        folder = cursor.fetchall()
        conn.close()
        return folder

    def remove_folder(self, folder_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Remove all bookmark in the folder
        cursor.execute('DELETE FROM bookmark WHERE folder_id = ?', (folder_id,))

        # Remove the folder itself
        cursor.execute('DELETE FROM folder WHERE id = ?', (folder_id,))

        conn.commit()
        conn.close()
