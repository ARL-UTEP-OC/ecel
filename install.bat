REM Make sure path to pip is set correctly and CMD.exe is running with administrative privileges.

SET "ECEL_DIR=%cd%"
SET OUTPUT_PREFIX=ECEL INSTALLER:
SET OUTPUT_ERROR_PREFIX=%OUTPUT_PREFIX% ERROR:

rem Download chocolatey (windows package manager. "apt-get")
rem After initial download, ensure that chocolatey is installed in C:\ProgramData (or change to whatever directory it becomes installed in.
IF NOT EXIST %ProgramData%\chocolatey ( @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin")

set REQUIRED_PLUGINS=nmap,wireshark
echo Installing dependencies (Snoopy will not be installed-Linux only)

for %%p in ("%REQUIRED_PLUGINS:,=" "%") do choco install %%p

rem Wireshark installs by default in C:\Program Files (64 bit directory), while Nmap installs in C:\Program Files x86 (32 bit directory)
rem These may need to be changed depending on where chocolatey installs nmap/tshark on your machine. CHeck Program files/Program files x86.
set path=%path%;%ProgramFiles%\Wireshark
set path=%path%;%ProgramFiles(x86)%\Nmap

echo Installing python dependencies

rem it may be necessary to download some of these packages manually if pip install does not work.
rem ensure these packages are installed in your site-packages folder for your current versoin of python.
set PYTHON_DEPENDENCIES=virtualenv,enum34,psutil,netifaces,autopy
for %%p in ("%PYTHON_DEPENDENCIES:,=" "%") do pip install %%p

echo Creating Plugin Configs
for /D %%d in (.\plugins\collectors\*) do copy %%d\config.json.template %%d\config.json & copy %%d\config_schema.json.template %%d\config_schema.json

echo %OUTPUT_PREFIX% Compiling parsers

rem make sure path to javac command is up to date. This is needed to compile parser code.
set path=%path%;%ProgramFiles%\Java\jdk1.8.0_91\bin

for /D %%d in (.\plugins\parsers\*) do if exist %%d\*.java (javac %%d\*.java)

javac -cp .\plugins\parsers\nmap\java_classes\*.java

:prompt
::Clear the value of answer ready for use.
SET answer=
SET /P answer=Would you like to run ECEL automatically on login? (y/n):

IF %answer% == y (
    echo Adding ecel to start up...
    cd %ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup
    echo TODO: Add batch script that executes ecel in the start up folder
)

IF %answer% == n (
    echo Remove ecel from start up...
    cd %ProgramData%\Microsoft\Windows\Start Menu\Programs\
    echo TODO: Remove ecel batch script from start up folder
)

cd %ECEL_DIR%

echo For windows execution, the following must be installed manually: PyGobject, Gtk+ runtime, appindicator3
echo %OUTPUT_PREFIX% Installation Complete. Type "python ecel_gui.py" to start ECEL




