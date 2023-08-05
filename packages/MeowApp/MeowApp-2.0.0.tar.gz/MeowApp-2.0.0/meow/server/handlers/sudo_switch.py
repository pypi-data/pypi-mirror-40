

import os
import sys
import subprocess
from _signal import SIGTERM

from flask import Blueprint
from flask_json import json_response

sudo_switch_handler = Blueprint('sudo_switch_handler', __name__)


@sudo_switch_handler.route('/sudo')
def switch_to_sudo():
    # print(sys.argv[0])
    # res = os.execvp("pkexec", ["pkexec", f"{os.getcwd()}/meow.py"])
    # os.kill(os.getpid(), SIGTERM)
    # print(res)
    # print(f"{os.getcwd()}/meow.py")

    # subprocess.Popen(["pkexec", f"/home/nico/IdeaProjects/meow2/meow.py"])
    subprocess.Popen(["pkexec", f"{os.getcwd()}/meow.py"])
    return json_response(data_={
        "sudo": True
    })

