# Evaluator-Centric and Extensible Logger


###At this point of the project, the program has been tested in:
-(32-bit and 64-bit ) Kali Linux 2016.1 and 2016.2, both 32 and 64-bit

----------------
Installation
----------------
Execute the following to install:
 install.sh

----------------
Execution
----------------
Run the following command to exeute ECEL.
 ./ecel_gui

This will invoke the main GUI and a clickable status icon in the task bar.

-----------
Plugins
-----------

The ECEL is written using a plugin architecture. There are two types of plugins, collectors and parsers. Collector plugins will collect timestamps and event data. These collector plugins use custom or existing external
logging tools. Parser plugins read log data (that produced by the collectors) and then format the data into an alternate form. All plugins are managed (started, terminated, etc.) from the ECEL graphical interface.

The following are the plugins that come packaged with ECEL.
###PyKeylogger
-https://github.com/nanotube/pykeylogger

The collector plugin will execute pykeylogger to gather screenshots (on mouse clicks on based on a timer) and keystrokes.
The parser plugin executes three tasks. The first will read keystroke data and then, based on a time threshold/delimiter, weave the data into keystroke units and produce a labeled JSON file.
The second extracts mouse click screenshot paths and timestamps and stores them in a JSON file. Simiarly, the last task extracts timed screenshot paths and timestamps and stores them in a JSON file.

###tshark, multi_inc_tshark, and multi_exc_tshark
- https://www.wireshark.org/download.html

There are three collector plugins that leverage tshark. The first executes a single instance of tshark on a specified interface. The multi_inc_tshark will collect network data on all specified interfaces. Multi_exc_tshark will collect network data on all interfaces, except any specified.
The parser plugin will extract various protocol fields from network packtes including source and destination MAC, IP, and port information as well as flags (TCP) and routes (RIP).

###Snoopy
- https://github.com/a2o/snoopy

The collector plugin will gather all system calls on the system by leveraging the snoopy tool. The plugin reads the auth.log file produced by snoopy and will periodically copy it into the ECEL raw data folder.
The parser plugin will read the snoopy log and generate a set of timestamp/system call pairs formatted in a JSON file.

###Manual Screenshot
- http://www.autopy.org/documentation/api-reference/bitmap.html

The collector is a manual plugin that is executed by clickin on the context menu of the ECEL status icon. A dialog window will collect metadata and then take a screenshot using the autopy module.
With the parser plugin, all of the stored metadata is then formatted and stored in a JSON file.
