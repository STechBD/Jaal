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
app.static_folder = os.path.join(os.path.dirname(__file__), 'static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/home')
def home():
    return app.send_static_file('index.html')


@app.route('/img')
def img_dir():
    return 'Image not found'


@app.route('/img/<string:file>')
def img(file):
    return app.send_static_file('img/' + file)


@app.route('/js')
def js_dir():
    return 'JS not found'


@app.route('/js/<string:file>')
def js(file):
    return app.send_static_file('js/' + file)


@app.route('/css')
def css_dir():
    return 'CSS not found'


@app.route('/css/<string:file>')
def css(file):
    return app.send_static_file('css/' + file)


@app.route('/about', methods=['GET'])
def about():
    return 'Jaal is a web browser developed by S Technologies.<br/>Version: 1.0.0'


@app.route('/bookmark')
def bookmark():
    return app.send_static_file('bookmark.html')


@app.route('/get_folder', methods=['GET'])
def get_folders():
    parent_id = request.args.get('parent_id')
    folders = bookmark_manager.get_folder(parent_id)
    return jsonify([{'id': folder[0], 'name': folder[1], 'parent_id': folder[2]} for folder in folders])


@app.route('/add_folder', methods=['POST'])
def add_folder():
    data = request.get_json()
    name = data['name']
    parent_id = data['parent_id']
    bookmark_manager.add_folder(name, parent_id)
    return jsonify({'message': 'Folder added successfully'})


@app.route('/remove_folder', methods=['POST'])
def remove_folder():
    data = request.get_json()
    folder_id = data['id']
    bookmark_manager.remove_folder(folder_id)
    return jsonify({'message': 'Folder removed successfully'})


@app.route('/get_bookmark', methods=['GET'])
def get_bookmarks():
    folder_id = request.args.get('folder_id')
    bookmarks = bookmark_manager.get_bookmark(folder_id)
    return jsonify(
        [{'id': bookmark[0], 'title': bookmark[1], 'url': bookmark[2], 'favicon': bookmark[3]} for bookmark in
         bookmarks])


@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    data = request.get_json()
    title = data['title']
    url = data['url']
    folder_id = data['folder_id']
    favicon = data['favicon']
    bookmark_manager.add_bookmark(title, url, folder_id, favicon)
    return jsonify({'message': 'Bookmark added successfully'})


@app.route('/remove_bookmark', methods=['POST'])
def remove_bookmark():
    data = request.get_json()
    bookmark_id = data['id']
    bookmark_manager.remove_bookmark(bookmark_id)
    return jsonify({'message': 'Bookmark removed successfully'})


@app.route('/history')
def history():
    return app.send_static_file('history.html')


@app.route('/get_history')
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
    time = data['time']

    # Handle favicon correctly
    favicon = None
    if 'favicon' in data and isinstance(data['favicon'], str) and data['favicon']:
        try:
            favicon = base64.b64decode(data['favicon'])
        except (TypeError, ValueError) as e:
            print(f"Invalid favicon data: {e}")

    # Add history entry to database
    history_manager.add_history_entry(title, url, time, favicon)

    return jsonify({'message': 'History entry added successfully'})


@app.route('/remove_history', methods=['POST'])
def remove_history():
    data = request.get_json()
    history_id = data['id']
    history_manager.remove_history_entry(history_id)
    return jsonify({'message': 'History entry removed successfully'})


@app.route('/clear_history', methods=['POST'])
def clear_history():
    history_entries = history_manager.get_history()
    for entry in history_entries:
        history_manager.remove_history_entry(entry[0])
    return jsonify({'message': 'History cleared successfully'})


if __name__ == '__main__':
    app.run(port=5000)
