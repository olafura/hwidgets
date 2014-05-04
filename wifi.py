import gobject
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import json
from mapping import wifi_states
import couchdb
import ConfigParser
import time
import datetime
from conf import getUsernamePassword

username, password = getUsernamePassword()
couch = couchdb.Server()
couch.resource.credentials = (username,password)
db = couch["wifi"]

DBusGMainLoop(set_as_default=True)
loop = gobject.MainLoop()
import NetworkManager
bus = dbus.SystemBus()

currentdev = None

for device in NetworkManager.NetworkManager.GetDevices():
    if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
        currentdev = device.SpecificDevice()
        break

def getAP(point, active_op):
        try:
            doc = db[point.Ssid]
        except couchdb.http.ResourceNotFound:
            doc = {}
        doc["_id"] = point.Ssid
        is_active = point.object_path == active_op
        n = datetime.datetime.now()
        #I'm using unix time bacause it makes it easy to do math
        unix_time = time.mktime(n.timetuple())
        if "time" in doc:
            doc["last_time"] = doc["time"]
        doc["time"] = unix_time
        doc["is_active"] = is_active
        doc["strength"] = int(point.proxy.Get(point.interface_name, "Strength",dbus_interface="org.freedesktop.DBus.Properties"))
        return doc


def checkAccessPoints():
    if not currentdev == None:
        try:
            active = currentdev.ActiveAccessPoint
            access_points = currentdev.GetAccessPoints()
        except dbus.exceptions.DBusException:
            return
        active_op = active.object_path
        for point in access_points:
            doc = getAP(point, active_op)
            db.save(doc)
    #print "end"

def handle_apadded(ap):
    print("new_ap")
    active = currentdev.ActiveAccessPoint
    active_op = active.object_path
    doc = getAP(ap, active_op)
    db.save(doc)
    #print ap

def handle_apremove(ap):
    print("delete_ap")

currentdev.connect_to_signal("AccessPointAdded", handle_apadded)
currentdev.connect_to_signal("AccessPointRemoved", handle_apremove)

loop.run()
