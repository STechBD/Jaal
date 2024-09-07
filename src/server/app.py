import base64
import os
import sys
from datetime import datetime

from flask import Flask, request, jsonify

# Add the project root to the Python path to handle imports correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib.bookmark import Bookmark
from src.lib.history import History

app = Flask(__name__)
bookmark_manager = Bookmark()
history_manager = History()


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Jaal'

@app.route('/about', methods=['GET'])
def about():
    return 'Jaal is a web browser developed by S Technologies.<br/>Version: 1.0.0'


@app.route('/get_folders', methods=['GET'])
def get_folders():
    parent_id = request.args.get('parent_id')
    folders = bookmark_manager.get_folders(parent_id)
    return jsonify([{'id': folder[0], 'name': folder[1], 'parent_id': folder[2]} for folder in folders])


@app.route('/get_bookmarks', methods=['GET'])
def get_bookmarks():
    folder_id = request.args.get('folder_id')
    bookmarks = bookmark_manager.get_bookmarks(folder_id)
    return jsonify(
        [{'id': bookmark[0], 'title': bookmark[1], 'url': bookmark[2], 'favicon': bookmark[3]} for bookmark in
         bookmarks])


@app.route('/get_history', methods=['GET'])
def get_history():
    history_entries = history_manager.get_history()
    history_list = []
    for entry in history_entries:
        history_list.append({
            'id': entry[0],
            'title': entry[1],
            'url': entry[2],
            'time': entry[3],
            'favicon': base64.b64encode(entry[4]).decode('utf-8') if entry[4] else None
        })
    return jsonify(history_list)


@app.route('/add_history', methods=['POST'])
def add_history():
    data = request.get_json()
    title = data['title']
    url = data['url']
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    favicon = base64.b64decode(data['favicon']) if 'favicon' in data else None
    history_manager.add_history_entry(title, url, time, favicon)
    return jsonify({'message': 'History entry added successfully'})


@app.route('/remove_history', methods=['POST'])
def remove_history():
    data = request.get_json()
    history_id = data['id']
    history_manager.remove_history_entry(history_id)
    return jsonify({'message': 'History entry removed successfully'})


if __name__ == '__main__':
    app.run(port=5000)
