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
#I have to keep track of the access points because dbus deletes the
#information
current_access_points = {}

#A simple class simulate simulate the access point information
class AP(object):
    Ssid = ""
    object_path = ""

    def __init__(self, Ssid, object_path):
        self.Ssid = Ssid
        self.object_path = object_path

for device in NetworkManager.NetworkManager.GetDevices():
    if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
        currentdev = device.SpecificDevice()
        break

def getAP(point, active_op, available):
        print("point op", str(point.object_path))
        print("active op", str(active_op))
        try:
            doc = db[point.Ssid]
        except couchdb.http.ResourceNotFound:
            doc = {}
        doc["_id"] = point.Ssid
        is_active = str(point.object_path) == str(active_op)
        doc["is_available"] = available
        doc["is_active"] = is_active
        if available:
            new_ap = AP(str(point.Ssid),str(point.object_path))
            current_access_points[point.object_path] = new_ap
            doc["strength"] = int(point.proxy.Get(point.interface_name, "Strength",dbus_interface="org.freedesktop.DBus.Properties"))
        else:
            doc["strength"] = 0
        return doc


def checkAccessPoints():
    if not currentdev == None:
        try:
            active = currentdev.ActiveAccessPoint
            access_points = currentdev.GetAccessPoints()
        except dbus.exceptions.DBusException:
            return
        active_op = active.object_path
        ap_docs = []
        for point in access_points:
            doc = getAP(point, active_op, True)
            ap_docs.append(doc)
        #I use bulk update so I spend less time updating the access points
        #and less events
        db.update(ap_docs)
    #print "end"

checkAccessPoints()

def handle_apadded(ap):
    #print("new_ap")
    #print("ap", ap)
    active = currentdev.ActiveAccessPoint
    active_op = active.object_path
    doc = getAP(ap, active_op, True)
    db.save(doc)
    #print ap

def handle_apremove(ap):
    #print("delete_ap")
    #print("ap", ap)
    new_ap = current_access_points[ap.object_path]
    #by defination a deleted access_point can't be the current accesspoint
    #that's why I pass False as the second argument
    doc = getAP(new_ap, False, False)
    #print("doc",doc)
    db.save(doc)

currentdev.connect_to_signal("AccessPointAdded", handle_apadded)
currentdev.connect_to_signal("AccessPointRemoved", handle_apremove)

loop.run()
