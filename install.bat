cls
REM Make sure path to pip is set correctly and CMD.exe is running with administrative privileges.
net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Installing ECEL for windows...
    ) else (
        echo Please run cmd as an admin
    )

SET "ECEL_DIR=%cd%"
SET JAVAC_DIR=C:\Program Files\Java\jdk1.8.0_91\bin
SET OUTPUT_PREFIX=ECEL INSTALLER:
SET OUTPUT_ERROR_PREFIX=%OUTPUT_PREFIX% ERROR:


echo Creating Plugin Configs
for /D %%d in (.\plugins\collectors\*) do copy %%d\config.json.template %%d\config.json & copy %%d\config_schema.json.template %%d\config_schema.json

echo %OUTPUT_PREFIX% Compiling parsers
set path="%path%;%JAVAC_DIR%;"
for /D %%d in (.\plugins\parsers\*) do if exist %%d\*.java (javac %%d\*.java)




echo %OUTPUT_PREFIX% Installation Complete.

