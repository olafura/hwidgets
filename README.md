HWidgets a simple example of battery and wifi service
======================================================

It uses CouchDB as the backend service for the application, there is an
example web apps that polls data from CouchDB to update to the interace.

The backend uses DBus as it gets the most reliable access to underlying data.
I'm using the UPower and Network Manager services and polling data from them.
