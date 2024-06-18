# 2024-06-18
# Remmina 1.4.35

# Displays a clickable button in a Remmina Tabbed Protocol window

import sys
import inspect
#import rich

if not hasattr(sys, 'argv'):
    sys.argv = ['']

import remmina
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import psutil

class HelloPlugin:
    def __init__(self):
        self.name = "toolsdevler: Python Hello Plugin"
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

    def init(self, gp):
        print("toolsdevler: init!")
        return True

    #gp is remmina.RemminaProtocolWidget
    def open_connection(self, gp):
        print("toolsdevler: open_connection!")
        remmina.log_print("[%s]: toolsdevler: open connection\n" % self.name)
        print(sys.version)
        
        def foreach_child(child):
            child.add(self.btn)
            self.btn.show()
            
        gtkviewport = gp.get_viewport()
        gtkviewport.foreach(foreach_child)
        print("toolsdevler: Connected!")
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
        # The user requested to close the connection.
        remmina.protocol_plugin_signal_connection_closed(viewport)
        return True

    def query_feature(self):
        pass

    def call_feature(self, gp, feature):
        pass

    def send_keystrokes(self):
        pass

    def get_plugin_screenshot(self):
        pass

    def map_event(self, gp):
        # This is called when the widget is again on screen.
        return True

    def unmap_event(self, gp):
        # This is called when the widget is again not being shown on screen anymore. Any intensive graphical output
        # can be halted.
        return True

myPlugin = HelloPlugin()
remmina.register_plugin(myPlugin)

