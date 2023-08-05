from flask import Blueprint
from flask import send_from_directory

file_server_handler = Blueprint('file_server_handler', __name__)


@file_server_handler.route('/<path:path>')
def send_js(path):
    return send_from_directory('www', path)
