HWidgets a simple example of battery and wifi service
======================================================

It uses CouchDB as the backend service for the application, there is an
example web apps that polls data from CouchDB to update to the interace.

The backend uses DBus as it gets the most reliable access to underlying data.
I'm using the UPower and Network Manager services and polling data from them.

On a Ubuntu machine you just have to do a "make" command on the command-line
to do the initalizing and running of the application. After that you can use
"make run". You then use "make kill" to stop them. This creates a webserver
that runs on localhost:8000 and you can go there to access the web application.

Implementation details
----------------------
web/source/App.js contains the web user interface which is written in Enyo.js
battery.py contains the polling of the battery through UPower
wifi.py contains the polling of the wifi through Network Manager
