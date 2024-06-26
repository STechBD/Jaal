from flask import Flask, request, jsonify

from ..lib.bookmark import Bookmark


app = Flask(__name__)
bookmark_manager = Bookmark()


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


if __name__ == '__main__':
    app.run(port=5000)
