import sqlite3


class Bookmark:
    def __init__(self, db_path='bookmarks.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create the bookmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                favicon BLOB,
                folder_id INTEGER,
                FOREIGN KEY (folder_id) REFERENCES folders(id)
            )
        ''')

        # Create the folders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES folders(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_bookmark(self, title, url, favicon=None, folder_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmarks (title, url, favicon, folder_id) VALUES (?, ?, ?, ?)',
                       (title, url, favicon, folder_id))
        conn.commit()
        conn.close()

    def get_bookmarks(self, folder_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if folder_id:
            cursor.execute('SELECT id, title, url, favicon, folder_id FROM bookmarks WHERE folder_id = ?', (folder_id,))
        else:
            cursor.execute('SELECT id, title, url, favicon, folder_id FROM bookmarks WHERE folder_id IS NULL')
        bookmarks = cursor.fetchall()
        conn.close()
        return bookmarks

    def remove_bookmark(self, bookmark_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
        conn.commit()
        conn.close()

    def add_folder(self, name, parent_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO folders (name, parent_id) VALUES (?, ?)', (name, parent_id))
        conn.commit()
        conn.close()

    def get_folders(self, parent_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if parent_id:
            cursor.execute('SELECT id, name, parent_id FROM folders WHERE parent_id = ?', (parent_id,))
        else:
            cursor.execute('SELECT id, name, parent_id FROM folders WHERE parent_id IS NULL')
        folders = cursor.fetchall()
        conn.close()
        return folders

    def remove_folder(self, folder_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Remove all bookmarks in the folder
        cursor.execute('DELETE FROM bookmarks WHERE folder_id = ?', (folder_id,))

        # Remove the folder itself
        cursor.execute('DELETE FROM folders WHERE id = ?', (folder_id,))

        conn.commit()
        conn.close()
