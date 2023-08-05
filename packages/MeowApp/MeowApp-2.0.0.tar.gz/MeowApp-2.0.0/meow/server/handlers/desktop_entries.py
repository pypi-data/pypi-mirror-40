import hashlib
import os
from glob import glob

import gi
from flask import Blueprint, send_file, request

from flask_json import json_response, as_json
from xdg import DesktopEntry
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import shlex

desktop_entries_handler = Blueprint('desktop_entries_handler', __name__)


@desktop_entries_handler.route('/desktop_entries', methods=['GET'])
def list_desktop_entries():
    update_entries()
    return json_response(data_=desktop_entries)


@desktop_entries_handler.route('/desktop_entries/<entry_id>', methods=['GET'])
def get_desktop_entry(entry_id):
    return json_response(data_=get_entry_by_id(entry_id))


@desktop_entries_handler.route('/is_sudo')
def is_sudo():
    return json_response(data_={"is_sudo": os.geteuid() == 0})


@desktop_entries_handler.route('/desktop_entries/<entry_id>', methods=['POST'])
def update_desktop_entry(entry_id):
    body = request.get_json()
    print(body)
    path = body['path']
    de = DesktopEntry.DesktopEntry(path)
    de.set("Name", body['name'])

    if 'categories' in body:
        de.set("Categories", ";".join(body['categories']))

    if 'keywords' in body:
        de.set("Keywords", ";".join(body['keywords']))

    if 'hidden' in body:
        de.set("Hidden", str(body['hidden']).lower())

    try:
        de.write(path)
    except PermissionError:
        # subprocess.Popen(["pkexec", f"{os.getcwd()}/meow.py"])
        subprocess.Popen(["pkexec", f"meow_server"])
        return json_response(data_={
            "error": "Require root access"
        }, status_=401)

    update_entries()

    print(f"Should update {entry_id}")
    return json_response(data_=get_entry_by_id(entry_id))


@desktop_entries_handler.route('/icon/<entry_id>', methods=['GET'])
def get_desktop_entry_icon(entry_id):
    elems = entry_id.split('.')
    icon_path = None
    if len(elems) == 2:
        entry = get_entry_by_id(elems[0])
        if entry is not None and 'icon' in entry:
            icon_path = get_icon_path(entry['icon'])
    try:
        return send_file(icon_path)
    except Exception as e:
        return str(e)

    print(f"Should update {entry_id}")
    return json_response(data_=get_entry_by_id(entry_id))


@desktop_entries_handler.route('/run/<entry_id>', methods=['GET'])
def run_desktop_entry(entry_id):
    entry = get_entry_by_id(entry_id)

    elems = shlex.split(entry['exec'])
    if elems[-1].lower() == '%u':
        elems = elems[:-1]

    use_terminal = False
    if 'terminal' in entry:
        use_terminal = entry['terminal']
    print(use_terminal)

    if use_terminal:
        elems.insert(0, '--')
        elems.insert(0, 'gnome-terminal')
        # elems = 'gnome-terminal' + elems
        # elems = '--' + elems

    print(elems)
    subprocess.Popen(elems)
    return json_response(data_= {
        'running': True
    })


@desktop_entries_handler.route('/desktop_entries/<entry_id>', methods=['DELETE'])
def delete_desktop_entry(entry_id):
    print(f"Should delete {entry_id}")
    is_found = False
    is_deleted = False

    entry = get_entry_by_id(entry_id)

    if entry is not None and 'path' in entry:
        desktop_entry_path = entry['path']
        print(f"Should delete {desktop_entry_path}")
        for desktop_path in desktop_paths:
            for path in glob(f"{desktop_path['path']}/**/*.desktop", recursive=True):
                if desktop_entry_path == path:
                    is_found = True
                    try:
                        print(desktop_entry_path)
                        proc = subprocess.Popen(["pkexec", "rm", desktop_entry_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        (output, err) = proc.communicate()
                        print(proc.returncode)

                        # proc.returncode
                        # if entry['require_admin']:
                        #     subprocess.Popen(["pkexec", "rm", desktop_entry_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        # else:
                        #     os.remove(desktop_entry_path)
                        is_deleted = True
                    except:
                        print("Need root access")
                        pass
    return json_response(data_={
        "found": is_found,
        "deleted": is_deleted
    })


def get_entry_by_id(entry_id):
    if entry_id in desktop_entry_cache:
        return desktop_entry_cache[entry_id]
    else:
        update_entries()
        if entry_id in desktop_entry_cache:
            return desktop_entry_cache[entry_id]
        else:
            return None


icon_theme = Gtk.IconTheme.get_default()
home_folder = os.getenv("HOME")
desktop_paths = [{
    "path": f"{home_folder}/.local/share/applications/",
    "require_admin": False
}, {
    "path": "/usr/share/applications",
    "require_admin": True
}, {
    "path": "/usr/local/share/applications",
    "require_admin": True
}]

desktop_entry_cache = {}
desktop_entries = []
response = None


def get_icon_path(icon):
    if os.path.isfile(icon):
        return icon
    else:
        icon_info = icon_theme.lookup_icon(icon, 128, 0)
        if icon_info is not None:
            return icon_info.get_filename()
        else:
            return None


def update_entries():
    desktop_entry_cache.clear()
    desktop_entries.clear()
    for desktop_path in desktop_paths:
        for path in glob(f"{desktop_path['path']}/**/*.desktop", recursive=True):
            desktop_entry = DesktopEntry.DesktopEntry(path)
            desktop_entry_id = hashlib.md5(desktop_entry.getFileName().encode()).hexdigest()
            if 'Desktop Entry' in desktop_entry.content:
                icon_path = get_icon_path(desktop_entry.getIcon())
                icon_img = None
                if icon_path is not None:
                    icon_extension = icon_path.split('.')[-1]
                    icon_img = desktop_entry_id + '.' + icon_extension
                desktop_entry_full = {
                    "id": desktop_entry_id,
                    "require_admin": desktop_path['require_admin'],
                    "path": desktop_entry.getFileName(),
                    "name": desktop_entry.getName(),
                    "generic_name": desktop_entry.getGenericName(),
                    "exec": desktop_entry.getExec(),
                    "icon": desktop_entry.getIcon(),
                    "icon_img": icon_img,
                    "hidden": desktop_entry.getHidden(),
                    "not_show_in": desktop_entry.getNotShowIn(),
                    "no_display": desktop_entry.getNoDisplay(),

                    "categories": desktop_entry.getCategories(),
                    "keywords": desktop_entry.getKeywords(),

                    "actions": desktop_entry.getActions(),
                    "binary_pattern": desktop_entry.getBinaryPattern(),
                    "comment": desktop_entry.getComment(),
                    "startup_notify": desktop_entry.getStartupNotify(),
                    "sort_order": desktop_entry.getSortOrder(),
                    "default_app": desktop_entry.getDefaultApp(),
                    "dev": desktop_entry.getDev(),
                    "doc_path": desktop_entry.getDocPath(),
                    "terminal": desktop_entry.getTerminal(),
                    "terminal_options": desktop_entry.getTerminalOptions(),
                    "version": desktop_entry.getVersion(),
                    "type": desktop_entry.getType(),
                    "url": desktop_entry.getURL(),
                    "try_exec": desktop_entry.getTryExec(),
                    "mimtypes": desktop_entry.getMimeTypes(),
                    # "entry": DesktopEntry.DesktopEntry(path).content['Desktop Entry']
                }
                desktop_entry_short = {
                    "id": desktop_entry_id,
                    "require_admin": desktop_path['require_admin'],
                    "path": desktop_entry.getFileName(),
                    "name": desktop_entry.getName(),
                    "icon_img": icon_img,
                    "hidden": desktop_entry.getHidden(),
                    "not_show_in": desktop_entry.getNotShowIn(),
                    "no_display": desktop_entry.getNoDisplay(),
                }
                desktop_entries.append(desktop_entry_short)
                desktop_entry_cache[desktop_entry_id] = desktop_entry_full

