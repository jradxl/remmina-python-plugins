# 2024-06-16
# Remmina 1.4.35

import sys
import remmina
import enum
import gi
import inspect
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

"""
   Internal data struct to hold ids to feature settings.
"""
class VncFeature:
    PrefQuality = 1
    PrefViewonly = 2
    PrefDisableserverinput = 3
    ToolRefresh = 4
    ToolChat = 5
    ToolSendCtrlAltDel = 6
    Scale = 7
    Unfocus = 8

"""
   Internal data struct to hold state.
"""
class VncData:
    def __init__(self):
        self.connected = False
        self.running = False
        self.auth_called = False
        self.auth_first = False
        self.drawing_area = False
        self.vnc_buffer = False
        self.rgb_buffer = False

"""
   Plugin implementation
"""
class Plugin:
    def __init__(self):
        # This constructor is called before Remmina attempts to register the plugin since it this class has to be instantiated before registering it.
        # A short name of the plugin that also appears in the 'Plugin' column in the main dialog.
        self.name = "Python Protocol Plugin VNC"
        # One of possible values: "pref", "tool", "entry", "protocol" or "secret". This value decides which methods are expected to be defined
        # in this class.
        self.type = "protocol"
        #Description appears in the Combo box
        self.description = "Protocol Plugin Example VNC"
        self.version = "1.0"
        self.icon_name = "org.remmina.Remmina-vnc-symbolic"
        self.icon_name_ssh = "org.remmina.Remmina-vnc-ssh-symbolic"
        # Specifies which settings are available for this protocol
        self.ssh_setting = remmina.PROTOCOL_SSH_SETTING_TUNNEL

        self.gpdata = VncData()
        self.qualities = ("0", "Poor Pixelmess", "1","Mhh kayy", "2","Nice", "9","hot sh*t")
        # Define the features this module supports:
        self.features = [
            remmina.Feature(
                type=remmina.PROTOCOL_FEATURE_TYPE_PREF,
                id=VncFeature.PrefQuality,
                opt1=remmina.PROTOCOL_FEATURE_PREF_RADIO,
                opt2="quality",
                opt3=self.qualities)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_PREF, VncFeature.PrefViewonly, remmina.PROTOCOL_FEATURE_PREF_CHECK, "viewonly", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_PREF, VncFeature.PrefDisableserverinput, remmina.PROTOCOL_SETTING_TYPE_CHECK, "disableserverinput", "Disable server input")
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, VncFeature.ToolRefresh, "Refresh", "face-smile", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, VncFeature.ToolChat, "Open Chat…", "face-smile", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, VncFeature.ToolSendCtrlAltDel,     "Send Ctrl+Alt+Delete", None, None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_SCALE, VncFeature.Scale, None, None, None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_UNFOCUS, VncFeature.Unfocus, None, None, None)
        ]

        colordepths = ("8", "256 colors (8 bpp)", "16", "High color (16 bpp)", "32", "True color (32 bpp)")
        self.basic_settings = [
            remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SERVER,  name="server",    label="",             compact=False, opt1="_rfb._tcp",opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_TEXT,    name="proxy",     label="Repeater",     compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_TEXT,    name="username",  label="Username",     compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_PASSWORD,name="password",  label="User password",compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SELECT,  name="colordepth",label="Color depth",  compact=False, opt1=colordepths,opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SELECT,  name="quality",   label="Quality",      compact=False, opt1=self.qualities, opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_KEYMAP,  name="keymap",    label="",             compact=False, opt1=None,       opt2=None)
        ]
        self.advanced_settings = [
            remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "showcursor",             "Show remote cursor",       True,  None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "viewonly",               "View only",                False, None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "disableclipboard",       "Disable clipboard sync",   True,  None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "disableencryption",      "Disable encryption",       False, None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "disableserverinput",     "Disable server input",     True,  None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "disablepasswordstoring", "Disable password storing", True, None, None)
            , remmina.Setting(remmina.PROTOCOL_SETTING_TYPE_CHECK, "disablesmoothscrolling", "Disable smooth scrolling", True, None, None)
        ]

    def init(self, gp):
        # this is called when the plugin is loaded from Remmina.
        cfile = gp.get_file()
        self.gpdata.disable_smooth_scrolling = cfile.get_setting(key="disablesmoothscrolling", default=False)
        self.gpdata.drawing_area = gp.get_viewport()
        return True

    def open_connection(self, gp):
        # Is called when the user wants to open a connection whith this plugin.

        # Write code to initiate the connection. Example:
        connection_file = gp.get_file()
        connection_file.set_setting("disablepasswordstoring", False)
        password = None

        # Determine if passwords should not be allowed to be stored.
        dont_save_passwords = connection_file.get_setting("disablepasswordstoring", False)
        # Open a dialog prompting connection information and credentials
        ret = remmina.protocol_plugin_init_auth(widget=gp,
                                                flags= remmina.REMMINA_MESSAGE_PANEL_FLAG_USERNAME | remmina.REMMINA_MESSAGE_PANEL_FLAG_USERNAME_READONLY | remmina.REMMINA_MESSAGE_PANEL_FLAG_DOMAIN | remmina.REMMINA_MESSAGE_PANEL_FLAG_SAVEPASSWORD,
                                                title="Python Rocks!",
                                                default_username="",
                                                default_password=connection_file.get_setting("password", ""),
                                                default_domain="",
                                                password_prompt="Your Password Rocks!")

        # Process the result of the dialog
        if ret == Gtk.ResponseType.CANCEL:
            return False
        elif ret == Gtk.ResponseType.OK:
            # Indicate that the connection has been established!
            remmina.protocol_plugin_signal_connection_opened(gp)

        return True

    def close_connection(self, gp):
        # The user requested to close the connection.
        remmina.protocol_plugin_signal_connection_closed(gp)

    def query_feature(self, gp, feature):
        # Remmina asks if the given feature is available (remember Features registered in the construtor).
        return True

    def map_event(self, gp):
        # This is called when the widget is again on screen.
        return True

    def unmap_event(self, gp):
        # This is called when the widget is again not being shown on screen anymore. Any intensive graphical output
        # can be halted.
        return True

    def call_feature(self, gp, feature):
        # Remmina asks to execute on of the features.

        if feature.type == remmina.REMMINA_PROTOCOL_FEATURE_TYPE_PREF and feature.id is VncFeature.PrefQuality:
            file = gp.get_file()
            quality = file.get_setting("quality", 0)
            if quality == 9:
                print("Ramping up graphics. Enjoy!")
            if quality == 0:
                print("Squeezing image into a few pixels...")
            if quality == 1:
                print("More the average guy, eh?")
            if quality == 2:
                print("Not great, not terrible...")

    def send_keystrokes(self, gp, strokes):
        # Remmina received a key stroke and wants to pass it to the remote.
        return True

    def get_plugin_screenshot(self, gp, data):
        # data is of type RemminaScreenshotData and should contain the raw pixels for the screenshot. Remmina takes care of storing it into a jpg.
        # Return True when a screenshot has been done. Otherwise False.
        return False

# Instantiate & Register
myPlugin = Plugin()
remmina.register_plugin(myPlugin)

