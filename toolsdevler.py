# 2024-06-16
# Remmina 1.4.35

import sys

if not hasattr(sys, 'argv'):
    sys.argv = ['']

import remmina
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import psutil

class HelloPlugin:
    def __init__(self):
        self.name = "toolsdevler: Python Hello World Plugin"
        self.type = "protocol"
        self.description = "toolsdevler: Description!"
        self.version  = "1.0"
        self.icon_name = "org.remmina.Remmina-tool-symbolic"
        self.icon_name_ssh = "org.remmina.Remmina-tool-symbolic"
        self.btn = Gtk.Button(label="Hello!")
        self.btn.connect("clicked", self.callback_add, "hello")
        self.features = []
        self.basic_settings = []
        self.advanced_settings = []
        self.ssh_setting = ""
        pass

    def callback_add(self, widget, data):
        print("toolsdevler: Click!)")

    def name(self):
        return "toolsdevler: Hello!"

    def init(self):
        print("toolsdevler: init!")
        return True

    def open_connection(self, viewport):
        print("toolsdevler: open_connection!")
        def foreach_child(child):
            child.add(self.btn)
            self.btn.show()
        viewport.foreach(foreach_child)
        print("toolsdevler: Connected!")

        remmina.log_print("[%s]: toolsdevler: open connection\n" % self.name)
        return True

    def draw(self, widget, cr, color):
        cr.rectangle(0, 0, 100, 100)
        cr.set_source_rgb(color[0], color[1], color[2])
        cr.fill()
        cr.queue_draw_area(0, 0, 100, 100)

        return True

    def close_connection(self, viewport):
        print("toolsdevler: close_connection!")
        remmina.log_print("[%s]: Plugin close connection\n" % self.name)
        return True

    def query_feature(self):
        pass

    def call_feature(self, gp, feature):
        pass

    def send_keystrokes(self):
        pass

    def get_plugin_screenshot(self):
        pass

myPlugin = HelloPlugin()
remmina.register_plugin(myPlugin)

