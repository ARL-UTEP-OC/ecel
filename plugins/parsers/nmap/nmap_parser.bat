set xmlFilePath=%1
set outputFilePath=%2
set HOME_DIR=%3

set class_path=%HOME_DIR%\plugins\parsers\nmap\java_classes

for %%x in (%xmlFilePath%\*.xml) do java -cp %class_path% NmapDataParser %%x %outputFilePath%\test.JSON