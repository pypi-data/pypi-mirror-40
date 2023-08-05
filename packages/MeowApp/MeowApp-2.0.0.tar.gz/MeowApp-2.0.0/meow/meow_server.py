from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS
from .server.handlers.desktop_entries import desktop_entries_handler
from .server.handlers.kill import kill_handler
from .server.handlers.sudo_switch import sudo_switch_handler
from .server.handlers.file_serve_handler import file_server_handler

import os
import requests


def start_server(use_debug=False):
    port = 20100

    if os.geteuid() == 0:
        print("Run as root")
    else:
        print("Not root")

    if 'WERKZEUG_RUN_MAIN' in os.environ or os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        try:
            requests.get(f"http://localhost:{port}/kill", timeout=1).status_code
        except Exception:
            print("Unable to kill")
            pass

    print("Start app")
    app = Flask(__name__)
    FlaskJSON(app)
    CORS(app)

    app.register_blueprint(desktop_entries_handler)
    app.register_blueprint(kill_handler)
    app.register_blueprint(sudo_switch_handler)
    app.register_blueprint(file_server_handler)

    app.config.update({
        "JSON_ADD_STATUS": False
    })

    try:
        app.run(port=port, debug=use_debug)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    start_server(True)
