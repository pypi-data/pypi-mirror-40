import shlex
import shutil
import sys

import gi
from cefpython3 import cefpython as cef

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

def py_select_file(exec, js_callback):
    base_path = exec

    if base_path[0] != '/':
        path_parts = shlex.split(exec)
        base_path = shutil.which(path_parts[0])

    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    dialog = Gtk.FileChooserDialog("Please choose a file", win,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.set_keep_above(True)
    dialog.set_filename(base_path)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        js_callback.Call(dialog.get_filename())
    dialog.destroy()


foo = {
    'drop_js_callback': None
}


def py_register_drop_cb(js_callback):
    foo['drop_js_callback'] = js_callback


class DisplayHandler(object):
    def OnConsoleMessage(self, browser, message, line, **_):
        print(message)


class RequestHandler(object):
    def OnBeforeBrowse(self, browser, frame, request, user_gesture, is_redirect):
        request_url = request.GetUrl()
        print(request_url)
        if foo['drop_js_callback'] is not None:
            foo['drop_js_callback'].Call({
                'url': request_url,
                'is_file': True
            })
        return True


def start_gui():
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize({
        'cache_path': '.cefcache'
    })
    browser = cef.CreateBrowserSync(url="http://localhost:20100/index.html", window_title="Meow")

    bindings = cef.JavascriptBindings()
    bindings.SetFunction("select_file", py_select_file)
    bindings.SetFunction("register_drop_cb", py_register_drop_cb)
    browser.SetJavascriptBindings(bindings)
    browser.SetClientHandler(DisplayHandler())
    browser.SetClientHandler(RequestHandler())

    # Set window position
    display = Gdk.Display.get_default()
    device_manager = Gdk.Display.get_device_manager(display)
    pointer = device_manager.get_client_pointer()
    pos = pointer.get_position()
    browser.SetBounds(max(pos.x - 1280 / 2, 0), max(pos.y - 800 / 2, 0), 1280, 800)

    cef.MessageLoop()
    cef.Shutdown()


if __name__ == '__main__':
    start_gui()

