# 2024-06-16
# Remmina 1.4.35

# Note: init_order = 2001  The Secret plugin with lowest init_order will be loaded as default.
# Remmina's Secret plugin glibsecret has an init_order of 2000, hence this demo set to 2001

import remmina

class PluginSecret:
    def __init__(self):
        self.name = "Python Secret Plugin"
        self.pref_label = "Secret Plugin Label"
        self.type = "secret"
        self.description = "A neat secret plugin"
        self.version  = "1.0"
        # A password storage that stores passwords in memory (totally useless of course...).
        self.keys = {}
        self.init_order = 2001

    def init(self):
        return True

    def is_service_available(self):
        return True

    def store_password(self, file, key, pwd):
        self.keys[key] = pwd

    def get_password(self, file, key):
        return self.keys[key] if key in self.keys else ""

    def delete_password(self, file, key):
        self.keys[key] = None

mySecretPlugin = PluginSecret()
remmina.register_plugin(mySecretPlugin)

