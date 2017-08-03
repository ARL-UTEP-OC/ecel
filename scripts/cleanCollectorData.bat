SET "ECEL_DIR=%cd%"
SET COLLECTOR_DIR=%ECEL_DIR%\plugins\collectors\*

FOR /D  %%d IN (%COLLECTOR_DIR%) DO (
    del %%d\raw\*
    del %%d\raw\META\*
    del %%d\parsed\*
    del %%d\compressed\*
)
