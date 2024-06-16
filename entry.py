# 2024-06-16
# Remmina 1.4.35

import remmina

class PluginEntry:
    def name(self):
        return "Python Entry Plugin: Name function"
        
    def __init__(self):
        self.name = "Python Entry Plugin"
        self.type = "entry"
        self.description = "Python Entry Plugin: Hello World!"
        self.version  = "1.0"
                

myEntryPlugin = PluginEntry()
remmina.register_plugin(myEntryPlugin)

