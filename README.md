# Evaluator-Centric and Extensible Logger (ECEL)

## System Requirements
ECEL has been tested on:
* Kali Linux 2016.2, both 32 and 64-bit
* Ubuntu 16.04 LTS 64-bit*, but see caveat below
* Windows 8/10 64-bit, but see caveat(s) below

*ECEL must be run as root. In order for the task bar status icon to function properly, you must also be logged in as root.

## Installation
To install ECEL, run `./install.sh`. A internet connection is required for installation.

## Windows Installation (Tested on Windows 8/10, 64 bit machines)
To install ECEL on windows, complete the following steps in the exact order they are listed:
1. Install python -V 2.7.13. It is important that this is the only version of python installed on your machine, and that it is stored directly on your C:\ drive. (i.e. C:\Python27)
When you download python, ensure that pip is going to be installed, and that python is added to your %path% variable.
2. Download the windows GTK3 runtime installer here: https://sourceforge.net/projects/gtk3win/
3. Download the windows PyGObject installer (GTK3 packages) here: https://sourceforge.net/projects/pygobjectwin32/files/?source=navbar
4. Download autopy (python package that fails to install using pip) here: https://pypi.python.org/pypi/autopy/  (Install into C:\Python27\Lib\site-packages directory)
5. Edit the following line in your  install batch (install.bat) file: 'SET JAVAC_DIR=*INSERT JAVAC DIRECTORY HERE*'
*Make sure that the path specified is a path to a javac executable. This is needed so that the java parsing code gets compiled. (This step may not be necessary if javac is permanently added to your %path% variable, but if not it will be necessary to make this edit depending on your version of java)
6. Open the windows command prompt (as an administrator), and navigate to your home ecel directory.
7. Run the install file by typing 'install.bat' and hitting 'Enter'.

## Execution
Run `./ecel_gui` to execute ECEL. This will invoke the main GUI and a clickable status icon will appear in the task bar.

## Windows Excecution
Caveat: Before executing ECEL on windows, currently all code referencing 'AppIndicator3' and the status icon must be commented out.
A windows version of 'AppIndicator3' is being researched.
Run 'ecel_gui.bat' to execute ECEL on windows. This will invoke the main GUI.

## Plugins

The ECEL is written using a plugin architecture. There are two types of plugins, collectors and parsers. Collector plugins will collect timestamps and event data. These collector plugins use custom or existing external
logging tools. Parser plugins read log data (that produced by the collectors) and then format the data into an alternate form. All plugins are managed (started, terminated, etc.) from the ECEL graphical interface.

The following are the plugins that come packaged with ECEL.

### PyKeylogger

https://github.com/nanotube/pykeylogger

The collector plugin will execute pykeylogger to gather screenshots (on mouse clicks on based on a timer) and keystrokes.
The parser plugin executes three tasks. The first will read keystroke data and then, based on a time threshold/delimiter, weave the data into keystroke units and produce a labeled JSON file.
The second extracts mouse click screenshot paths and timestamps and stores them in a JSON file. Simiarly, the last task extracts timed screenshot paths and timestamps and stores them in a JSON file.

### tshark, multi_inc_tshark, and multi_exc_tshark

https://www.wireshark.org/download.html

There are three collector plugins that leverage tshark. The first executes a single instance of tshark on a specified interface. The multi_inc_tshark will collect network data on all specified interfaces. Multi_exc_tshark will collect network data on all interfaces, except any specified.
The parser plugin will extract various protocol fields from network packtes including source and destination MAC, IP, and port information as well as flags (TCP) and routes (RIP).

### Snoopy

https://github.com/a2o/snoopy

The collector plugin will gather all system calls on the system by leveraging the snoopy tool. The plugin reads the auth.log file produced by snoopy and will periodically copy it into the ECEL raw data folder.
The parser plugin will read the snoopy log and generate a set of timestamp/system call pairs formatted in a JSON file. This plugin will not work on windows.

### Manual Screenshot

http://www.autopy.org/documentation/api-reference/bitmap.html

The collector is a manual plugin that is executed by clickin on the context menu of the ECEL status icon. A dialog window will collect metadata and then take a screenshot using the autopy module.
With the parser plugin, all of the stored metadata is then formatted and stored in a JSON file.
