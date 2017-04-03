set filename=%1
set outputpath=%2
set clicksdirectory=%3
set timeddirectory=%4

java KeysToJSON %filename% %outputpath%
java ClicksToJSON %clicksdirectory% %outputpath%
java TimedToJSON %timeddirectory% %outputpath%
