# 2024-06-18
# Remmina 1.4.35
# Doesn't really attempt to make an X2go connection.
# Is just another protocol basic example.
# Dependancies
# In your current user account: pip install gevent
# In your current system, install:  sudo apt install pyhoca-gui pyhoca-cli

import sys
import remmina
import enum
import gi
import inspect
import psutil
import gevent
import x2go

from multiprocessing import Process
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class X2goFeature:
    PrefQuality = 1
    PrefViewonly = 2
    PrefDisableserverinput = 3
    ToolRefresh = 4
    ToolChat = 5
    ToolSendCtrlAltDel = 6
    Scale = 7
    Unfocus = 8

class X2goData:
    def __init__(self):
        self.connected = False
        self.running = False
        self.auth_called = False
        self.auth_first = False
        self.drawing_area = False
        self.vnc_buffer = False
        self.rgb_buffer = False
        
class Plugin:
    def __init__(self):
        #print("X2go: Class Init")
        # This constructor is called before Remmina attempts to register the plugin since it this class has to be instantiated before registering it. 
        self.name = "Python Protocol Plugin X2GO OLD"
        # One of possible values: "pref", "tool", "entry", "protocol" or "secret". This value decides which methods are expected to be defined
        # in this class.        
        self.type = "protocol"
        self.description = "Python X2Go Plugin: Old Version"
        self.version = "1.0"    

        self.icon_name = "org.remmina.Remmina-vnc-symbolic"
        self.icon_name_ssh = "org.remmina.Remmina-vnc-ssh-symbolic"
        # Specifies which settings are available for this protocol
        self.ssh_setting = remmina.PROTOCOL_SSH_SETTING_TUNNEL

        self.gpdata = X2goData()
 
        self.sessionTypes = ("0", "KDE", "1","GNOME", "2","LXDE", "3","LXQt", "4","XFCE", "5","MATE", "6", "UNITY", "7", "CINNAMON", 
                            "8", "TRINITY", "9", "OPENBOX", "10", "ICEWM", "11", "RDP connection", "12", "XDMCP")
        
        self.qualities = ("0", "Poor Pixelmess", "1","Mhh kayy", "2","Nice", "9","hot sh*t")
        
        # Define the features this module supports:
        self.features = [
            remmina.Feature(
                type=remmina.PROTOCOL_FEATURE_TYPE_PREF,
                id=X2goFeature.PrefQuality,
                opt1=remmina.PROTOCOL_FEATURE_PREF_RADIO,
                opt2="quality",
                opt3=self.qualities)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_PREF, X2goFeature.PrefViewonly, remmina.PROTOCOL_FEATURE_PREF_CHECK, "viewonly", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_PREF, X2goFeature.PrefDisableserverinput, remmina.PROTOCOL_SETTING_TYPE_CHECK, "disableserverinput", "Disable server input")
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, X2goFeature.ToolRefresh, "Refresh", "face-smile", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, X2goFeature.ToolChat, "Open Chat…", "face-smile", None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_TOOL, X2goFeature.ToolSendCtrlAltDel,     "Send Ctrl+Alt+Delete", None, None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_SCALE, X2goFeature.Scale, None, None, None)
            ,remmina.Feature(remmina.PROTOCOL_FEATURE_TYPE_UNFOCUS, X2goFeature.Unfocus, None, None, None)
        ]      

        colordepths = ("8", "256 colors (8 bpp)", "16", "High color (16 bpp)", "32", "True color (32 bpp)")
        self.basic_settings = [
            remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SERVER,    name="server",    label="",             compact=False, opt1="_rfb._tcp",opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_TEXT,    name="proxy",     label="Repeater",     compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_TEXT,    name="username",  label="Username",     compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_PASSWORD,name="password",  label="User password",compact=False, opt1=None,       opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SELECT,  name="sessionType",   label="Session type",      compact=False, opt1=self.sessionTypes, opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SELECT,  name="colordepth",label="Color depth",  compact=False, opt1=colordepths,opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_SELECT,  name="quality",   label="Quality",      compact=False, opt1=self.qualities, opt2=None)
            , remmina.Setting(type=remmina.PROTOCOL_SETTING_TYPE_KEYMAP,  name="keymap",    label="",             compact=False, opt1=None,       opt2=None)
        ]
        
        self.advanced_settings = [
        ]

    def init(self, gp):
        print("X2Go Plugin Init")
        # this is called when the plugin is loaded from Remmina.
        cfile = gp.get_file()
        self.gpdata.disable_smooth_scrolling = cfile.get_setting(key="disablesmoothscrolling", default=False)
        self.gpdata.drawing_area = gp.get_viewport()
        return True

    def x2go_connection(self, gp):
        connection_file = gp.get_file()
        connectionName = connection_file.get_setting("name", "")
        server = connection_file.get_setting("server", "")
        userName = connection_file.get_setting("Username", "user")
        password = connection_file.get_setting("User pas", "")
        sessionIndx = connection_file.get_setting("Session typ", "0")
        sessionType = self.sessionTypes[self.sessionTypes.index(sessionIndx)+1]
        serverPort = remmina.public_get_server_port(server= server, defaultport= 22)
        
        #Usage of x2go fails at compile time.
    #try:
        #s = x2go.session.X2GoSession(server=serverPort[0], port=serverPort[1])
        #s.set_server(serverPort[0])
        #s.set_port(serverPort[1])
        #s.connect(userName, password)
        #s.start(cmd=sessionType)
        #s.set_session_window_title(connectionName)
        #while True: gevent.sleep(1)
    #except:
        #print("X2Go: failed to connect")
          
    def open_connection(self, gp):
        print("X2Go: Open connection")
        print(sys.version)
        # Is called when the user wants to open a connection with this plugin.
        #p = Process(target=self.x2go_connection, args=(gp,))
        #p.start()
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

        if feature.type == remmina.PROTOCOL_FEATURE_TYPE_PREF and feature.id is X2goFeature.PrefQuality:
            file = gp.get_file()

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

