# Evaluator-Centric and Extensible Logger

###UI
- python ecel.py start
- python ecel.py parse

###GUI
- python ecel_gui.py

###At this point of the project, the program has been tested in:
- (32-bit and 64-bit) Windows 7 and Windows 10
- (32-bit) Kali Linux 


----------------
Linux Environment
----------------
You will need to install autopy. The easiest method thus far has been to run the following commands. 

```Shell
- $ sudo apt-get install libxtst-dev
- $ sudo pip install autopy
```
For 64 Bit Versions Only
If you do not plan on using the recommended installer, you may run into issues with pykeylogger. You will need to
ensure that you are running python 2.7 and have the latest libraries for the following modules

-dpkt

-Image

-Pil

It is also recommended to use the pykeylogger source code that is provided. 
Downloading and using an different pykeylogger source could result in pykeylogger
not working correctly. 

----------------
Windows Environment
----------------
The following installations are needed to run the system on a Windows machine.

###PYGTK 
System uses version: 2.24
- http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/

The specific link for this version is provided below:
pygtk-all-in-one-2.24.2.win32-py2.7.msi     2012-02-09 21:48   32M 
Direct Link 
- http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/pygtk-all-in-one-2.24.2.win32-py2.7.msi 

###AutoPy
System uses version: 0.51
- https://pypi.python.org/pypi/autopy/

Plugins
-----------
The following installations are needed to run the plugins on a Windows machichine. 

###Keylogger 
- PIL http://www.pythonware.com/products/pil/
- ConfigObj http://www.voidspace.org.uk/python/configobj.html
- pyHook https://sourceforge.net/projects/pyhook/
- PyWin32 https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/

###Tshark
- https://www.wireshark.org/download.html

###Nmap
- https://nmap.org/download.html#windows


After installing tShark and nmap from the links below follow the remaining steps:

1. In the Windows command prompt type: `tshark -D`
2. Copy the long string between brackets {} for "Wi-Fi" or "Ethernet"
3. In tShark's run.bat file, place between the brackets for \Device\NPF_{<enter here>}
4. In netscanner's config.json file enter all of the data listed into the file. 

(Step 1 & 2) (Example, all machines will differ in output)
```Shell
C:\Users\johnDoe>tshark -D
1. \Device\NPF_{12345...} (VMware Network Adapter VMnet1)
2. \Device\NPF_{0123456789-E123-A12 (Wi-Fi)
3. \\.\USBPcap1 (USBPcap1)
```

(Step 3) tshark - run.bat
```Batch
echo off
set output=%1
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%%MM%%DD%" & set "timestamp=%HH%%Min%%Sec%"
"C:\Program Files (x86)\Wireshark\tshark.exe" -i \Device\NPF_{123456789-1234-1234-1234-123456789} -w %output%\%datestamp%%timestamp%.pcap > NUL
echo on
```

(Step 4) netscanner - config.json 
```JSON
{ 
  "name": "netscanner",
  "type": "multi",
  "enabled": false,
  "parser": "plugins.netscanner.parser",
  "output": "raw",
  "arguments": [
    ["\\Device\\NPF_{123456789-1234-1234-1234-12345}", "VMware Network Adapter VMnet1"],
    ["\\Device\\NPF_{123456789-1234-1234-1234-12345}", "Wi-Fi"]
  ]
}
