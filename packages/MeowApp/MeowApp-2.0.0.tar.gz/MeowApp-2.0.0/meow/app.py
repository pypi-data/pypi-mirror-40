from .front import start_gui
from .meow_server import start_server
import threading


def run_all():
    threading.Thread(target=start_gui).start()
    threading.Thread(target=start_server).start()
