echo on
set pcapfilename=%1
set outputpath=%2
java NetworkDataParser %pcapfilename% %outputpath%