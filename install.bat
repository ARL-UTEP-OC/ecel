REM Make sure path to pip is set correctly and CMD.exe is running with administrative privileges.
net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Installing ECEL for windows...
    ) else (
        echo Please run cmd as an admin
    )

SET "ECEL_DIR=%cd%"
SET OUTPUT_PREFIX=ECEL INSTALLER:
SET OUTPUT_ERROR_PREFIX=%OUTPUT_PREFIX% ERROR:

IF NOT EXIST %ProgramData%\chocolatey ( @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin")

set REQUIRED_PLUGINS=nmap,wireshark

echo Installing dependencies
for %%p in ("%REQUIRED_PLUGINS:,=" "%") do choco install %%p

set path=%path%;%ProgramFiles%\Wireshark
set path=%path%;%ProgramFiles(x86)%\Nmap

echo Snoopy will not be installed-Linux only

echo Creating Plugin Configs
for /D %%d in (.\plugins\collectors\*) do copy %%d\config.json.template %%d\config.json & copy %%d\config_schema.json.template %%d\config_schema.json

echo %OUTPUT_PREFIX% Compiling parsers

rem make sure path to javac command is up to date
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
    echo TODO: Add batch script that executes ecel to the start up folder
)

IF %answer% == n (
    echo Remove ecel from start up...
    cd %ProgramData%\Microsoft\Windows\Start Menu\Programs\
    echo TODO: Remove ecel batch script from start up folder
)

cd %ECEL_DIR%

pip install virtualenv
virtualenv ecel-installer
ecel-installer\Scripts\activate & pip install flask & pip install pyvbox & pip install gevent & pip install pypiwin32 & pip install gobject & pip install psutil & pip install python-xlib & pip install dpkt & pip install schedule & pip install netifaces

echo %OUTPUT_PREFIX% Installation Complete.



