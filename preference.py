# 2024-06-16
# Remmina 1.4.35

#Outstanding Bug: Shows <class 'tuple'> in terminal window on registration

import remmina
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class Pluginpref:
    def __init__(self):
        # A button to be shown in the preference dialog in Remmina
        self.button = None
        self.name = "Python Preference Plugin"
        # The label of the tab on the left side of the preference dialog.
        self.pref_label = "Preference: Label"
        self.type = "pref"
        self.description = "Preference: description!"
        self.version  = "1.0"
        # Prepare the button to be shonw inside the preference tab
        self.button = Gtk.Button(label="Preference: Click Here")    
        #The word clicked is a signal name
        self.button.connect("clicked", self.on_button_clicked)

    def get_pref_body(self):
        # Remmina renders the preferences and requests the body of the preference tab.
        return self.button

    def on_button_clicked(self, btn):
        print("Preference: on_button_clicked!)")


myprefPlugin = Pluginpref()
remmina.register_plugin(myprefPlugin)

