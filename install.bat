REM Make sure path to pip is set correctly and CMD.exe is running with administrative privileges.

SET "ECEL_DIR=%cd%"
SET OUTPUT_PREFIX=ECEL INSTALLER:
SET OUTPUT_ERROR_PREFIX=%OUTPUT_PREFIX% ERROR:
SET START_UP_DIR=%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup
SET START_UP_FILE=%START_UP_DIR%\ecel_startup.bat

rem Download chocolatey (windows package manager. "apt-get")
rem After initial download, ensure that chocolatey is installed in C:\ProgramData (or change to whatever directory it becomes installed in.
IF NOT EXIST %ProgramData%\chocolatey ( @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin")

set REQUIRED_PLUGINS=nmap,wireshark
echo Installing dependencies (Snoopy will not be installed-Linux only)

for %%p in ("%REQUIRED_PLUGINS:,=" "%") do choco install %%p

rem Wireshark installs by default in C:\Program Files (64 bit directory), while Nmap installs in C:\Program Files x86 (32 bit directory)
rem These may need to be changed depending on where chocolatey installs nmap/tshark on your machine. CHeck Program files/Program files x86.
SET WIRESHARK_DIR=%ProgramFiles%\Wireshark
SET NMAP_DIR=%ProgramFiles(x86)%\Nmap
set path=%path%;%WIRESHARK_DIR%
set path=%path%;%NMAP_DIR%

echo Installing python dependencies

rem it may be necessary to download some of these packages manually if pip install does not work.
rem ensure these packages are installed in your site-packages folder for your current versoin of python.
set PYTHON_DEPENDENCIES=virtualenv,enum34,psutil,netifaces
for %%p in ("%PYTHON_DEPENDENCIES:,=" "%") do pip install %%p

echo Creating Plugin Configs
for /D %%d in (.\plugins\collectors\*) do copy %%d\config.json.template %%d\config.json & copy %%d\config_schema.json.template %%d\config_schema.json

rem Enter the location of a javac executable below. This is needed to compile parser code.
SET JAVAC_DIR=C:\Program Files\Java\jdk1.8.0_91\bin

echo %OUTPUT_PREFIX% Compiling parsers

set path=%path%;%JAVAC_DIR%

for /D %%d in (.\plugins\parsers\*) do if exist %%d\*.java (javac %%d\*.java)

javac -cp .\plugins\parsers\nmap\java_classes\*.java

:prompt
::Clear the value of answer ready for use.
SET answer=
SET /P answer=Would you like to run ECEL automatically on login? (y/n):

IF %answer% == y (
    echo python %ECEL_DIR%\ecel_gui.py > "%START_UP_FILE%"
)

IF %answer% == n (
    del %START_UP_FILE%
)

echo For windows execution, the following must be installed manually: PyGobject, Gtk+ runtime, appindicator3
echo %OUTPUT_PREFIX% Installation Complete. Type "python ecel_gui.py" to start ECEL




