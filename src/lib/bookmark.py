import json
import os


class Bookmark:
    def __init__(self, bookmarks_file='bookmarks.json'):
        """
        Constructor function to initialize the Bookmark manager.

        :param bookmarks_file: The file where bookmarks will be stored.
        :since: 1.0.0
        """
        self.bookmarks_file = bookmarks_file
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        """
        Load bookmarks from the bookmarks file.

        :return: A list of bookmarks.
        :since: 1.0.0
        """
        if os.path.exists(self.bookmarks_file):
            with open(self.bookmarks_file, 'r') as file:
                return json.load(file)
        return []

    def save_bookmarks(self):
        """
        Save bookmarks to the bookmarks file.

        :return: None
        :since: 1.0.0
        """
        with open(self.bookmarks_file, 'w') as file:
            json.dump(self.bookmarks, file, indent=4)

    def add_bookmark(self, url, title):
        """
        Add a bookmark.

        :param url: The URL of the bookmark.
        :param title: The title of the bookmark.
        :return: None
        :since: 1.0.0
        """
        if not self.is_bookmarked(url):
            self.bookmarks.append({'url': url, 'title': title})
            self.save_bookmarks()

    def remove_bookmark(self, url):
        """
        Remove a bookmark.

        :param url: The URL of the bookmark to remove.
        :return: None
        :since: 1.0.0
        """
        self.bookmarks = [b for b in self.bookmarks if b['url'] != url]
        self.save_bookmarks()

    def is_bookmarked(self, url):
        """
        Check if a URL is already bookmarked.

        :param url: The URL to check.
        :return: True if the URL is bookmarked, False otherwise.
        :since: 1.0.0
        """
        return any(b['url'] == url for b in self.bookmarks)

    def get_bookmarks(self):
        """
        Get the list of bookmarks.

        :return: A list of bookmarks.
        :since: 1.0.0
        """
        return self.bookmarks
