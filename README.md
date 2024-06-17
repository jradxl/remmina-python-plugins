# Remmina Python Plugins

The original of these Python Plugins are at: https://gitlab.com/Remmina/Remmina/-/wikis/Development/Plugin-Development/Python/

Version here are sort of working for Remmina 1.4.35
They appear in the application but not all do what they are intended to do.

Remmina plugins are located in: <your path>/remmina/plugins
such as /usr/lib/x86_64-linux-gnu/remmina/plugins in Ubuntu.

The library, remmina-plugin-python_wrapper.so, must be represent for the python plugin to load.
It is a dynamic loader. Just the *.py file needs to be present in same directory, coded to Remmina's Python API.
(I know, it does seem odd to put source files in a library path)

To enable generation of the remmina-plugin-python_wrapper.so, -DWITH_PYTHONLIBS=ON must be given to cmake.
This library is not present in Ubuntu Jammy's repository (as Remmina 1.4.25), but it is 
as remmina-plugin-python in Ubuntu Noble (as Remmina 1.4.35)

Execute Remmina as: G_MESSAGES_DEBUG=remmina ./remmina or just ./remmina in a terminal window.
Information about the loading and registration of the python plugin will be show in the terminal window,
along with any complie errors.


## entry.py
Supposed to show an entry in the Hamburger menu
API:
python_wrapper_entry.c:		entry_func

## file.py
Can't see this within application
API:
python_wrapper_file.c:		import_test_func
python_wrapper_file.c:	    import_func
python_wrapper_file.c:		export_test_func
python_wrapper_file.c:		export_func

## preference.py
An entry in the left hand column of the Preference menu item shows, but there is nothing to the right.
API:
python_wrapper_pref.c:	    get_pref_body

## protocol-VNC.py, pyvnc.py
Same plugin but different versions. Shows up as a protocol choice in New Connection Profile.
But VNC connect action is not tested.
API:
python_wrapper_protocol.c:	init
python_wrapper_protocol.c:	open_connection
python_wrapper_protocol.c:	close_connection
python_wrapper_protocol.c:	query_feature
python_wrapper_protocol.c:	call_feature
python_wrapper_protocol.c:	send_keystrokes
python_wrapper_protocol.c:	get_plugin_screenshot
python_wrapper_protocol.c:	map_event
python_wrapper_protocol.c:	unmap_event

## secret.py  
Registers as an additional secret plugin.
API:
python_wrapper_secret.c:	init
python_wrapper_secret.c:	is_service_available
python_wrapper_secret.c:	store_password
python_wrapper_secret.c:	get_password
python_wrapper_secret.c:	delete_password

## tool.py
Appears as a menu item in the Hamberger menu. If clicked a message can be seen in the terminal window.
API:
python_wrapper_tool.c:	    exec_func

## toolsdevler.py
Also a protocol plugin

## See Also:
The plugin builder https://www.muflone.com/remmina-plugin-builder/english/
is very useful for C language plugins.
There are many C plugin examples where the RustDesk plugin works

//End
June 2024

