SET "ECEL_DIR=%cd%"
SET COLLECTOR_DIR=%ECEL_DIR%\plugins\collectors\*

FOR /D  %%d IN (%COLLECTOR_DIR%) DO (
    del /F /Q %%d\raw\*
    del /F /Q %%d\raw\META\*
    del /F /Q %%d\parsed\*
    del /F /Q %%d\compressed\*
)
