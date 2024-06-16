# 2024-06-16
# Remmina 1.4.35

import remmina

class PluginTool:
    def __init__(self):
        self.button = None
        # The name shown in the plugin list
        self.name = "Python Tool Plugin"
        self.type = "tool"
        # The description will be the label of the menu item!
        self.description = "Tool Plugin: Press me!"
        self.version  = "1.0"

    def exec_func(self):
        print("Tool Plugin: exec_func has been called!")

myToolPlugin = PluginTool()
remmina.register_plugin(myToolPlugin)

