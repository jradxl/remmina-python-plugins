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
        #Press the Tool Plugin: Press me! entry in the Hamburger menu
        #This will be shown in the terminal window
        print("Tool Plugin: exec_func has been called!")
        #This will be shown in the Debugging Window, opened from the Debugging option in the Hamburger menu
        remmina.log_print("Tool Plugin: exec_func has been called! THIS IS A LOG_PRINT STATEMENT")  

myToolPlugin = PluginTool()
remmina.register_plugin(myToolPlugin)

