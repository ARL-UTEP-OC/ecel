REM Make sure path to pip is set correctly
pip install virtualenv
virtualenv ecel-installer
ecel-installer\Scripts\activate & pip install gobject & pip install psutil & pip install python-xlib & pip install dpkt & pip install schedule & pip install netifaces