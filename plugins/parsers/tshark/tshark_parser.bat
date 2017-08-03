echo on
set pcapfilepath=%1
set outputpath=%2

mergecap %pcapfilepath%\*.*cap* -w %pcapfilepath%\merged.pcap
java NetworkDataParser %pcapfilepath%\merged.pcap %outputpath%
del "%pcapfilepath%\merged.pcap"
