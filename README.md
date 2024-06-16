# Remmina Python Plugins

The original of this Python plugins are at: https://gitlab.com/Remmina/Remmina/-/wikis/Development/Plugin-Development/Python/

Version here are sort of working for Remmina 1.4.35
They appear in the application but not all do what they are intended to do.

Remmina plugins are located in: <your path>/remmina/plugins
such as /usr/lib/x86_64-linux-gnu/remmina/plugins in Ubuntu.

The library, remmina-plugin-python_wrapper.so, must be represent for the python plugin to load.
It is a dynamic loader. Just the *.py file needs to be represent, coded to Remmina's Python API
To enable generation of the remmina-plugin-python_wrapper.so, -DWITH_PYTHONLIBS=ON must be given to cmake
This library is not present in Ubuntu Jammy's repository (as Remmina 1.4.25), but it is 
as remmina-plugin-python in Ubuntu Noble (as Remmina 1.4.35)

Execute Remmina as: G_MESSAGES_DEBUG=remmina ./remmina or just ./remmina in a terminal window.
Information about the loading and registration of the python plugin will be show in the terminal window,
along with any complie errors.


## entry.py
Supposed to show an entry in the Hamburger menu

## file.py
Can't see this within application

## preference.py
An entry in the left hand column of the Preference menu item shows, but there is nothing to the right.

## protocol-VNC.py, pyvnc.py
Same plugin but different versions. Shows up as a protocol choice in New Connection Profile.
But VNC connect action is not tested.

## secret.py  
Registers as an additional secret plugin.

## tool.py
Appears as a menu item in the Hamberger menu. If clicked a message can be seen in the terminal window.

## toolsdevler.py
Also a protocol plugin

## See Also:
The plugin builder https://www.muflone.com/remmina-plugin-builder/english/
is very useful for C language plugins.
There are many C plugin examples where the RustDesk plugin works

//End
June 2024

