import os
from signal import SIGTERM

from flask import Blueprint

kill_handler = Blueprint('kill_handler', __name__)

@kill_handler.route('/kill')
def kill_server():
    os.kill(os.getpid(), SIGTERM)

