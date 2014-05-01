import gobject
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import json
import datetime
import ConfigParser
import couchdb

DBusGMainLoop(set_as_default=True)
loop = gobject.MainLoop()
bus = dbus.SystemBus()
upower = bus.get_object("org.freedesktop.UPower","/org/freedesktop/UPower/devices/battery_BAT0")
upower_i = dbus.Interface(upower,dbus_interface="org.freedesktop.DBus.Properties")
properties = upower_i.GetAll("org.freedesktop.UPower.Device")
config = ConfigParser.RawConfigParser()
config.read("hwidgets.conf")
username = config.get("Server","username")
password = config.get("Server","password")
couch = couchdb.Server()
couch.resource.credentials = (username,password)
db = couch["battery"]

# I have to go through the properties because the json encoder does not
# support dbus.Double as a conversion unit
for key, value in properties.items():
        if isinstance(value, dbus.Double):
            properties[key] = float(value)

try:
    olddoc = db["battery"]
except couchdb.http.ResourceNotFound:
    olddoc = {}
doc = properties
#doc = json.dumps(properties)
doc["_id"] = "battery"
if "_rev" in olddoc:
    doc["_rev"] = olddoc["_rev"]
print("doc",doc)
db.save(doc)
upower = bus.get_object("org.freedesktop.UPower","/org/freedesktop/UPower")
def handle_notification(*args, **kwargs):
    print args, kwargs
upower.connect_to_signal("Changed", handle_notification)
loop.run()
