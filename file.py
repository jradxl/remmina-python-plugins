# 2024-06-16
# Remmina 1.4.35

import remmina

class Pluginfile:
    def __init__(self):
        self.name = "Python File Plugin"
        self.pref_label = "Preference Label"
        self.type = "file"
        self.description = " File: Drop something onto Remmina"
        self.version  = "1.0"
        self.export_hints = ".ttf"

    def import_test_func(self, file):
        # Test if we support this file.
        return True

    def import_func(self, path):
        # We promised to support the given file. Handle it:
        file = remmina.file_new()
        file.set_setting("name", path)
        file.set_setting("protocol", "PyVNC")
        # This file will appear as new entry in the list of stored connections in Remmina.
        return file

    def export_test_func(self, file):
        # Same as above but for export
        return True

    def export_func(self, file):
        # Same as above but for export
        return None


myfilePlugin = Pluginfile()
remmina.register_plugin(myfilePlugin)

