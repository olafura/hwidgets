#import gobject
#from dbus.mainloop.glib import DBusGMainLoop
import dbus
import json
from mapping import wifi_states
import couchdb
import ConfigParser
import time
import datetime
from conf import getUsernamePassword
#gobject.threads_init()

username, password = getUsernamePassword()
couch = couchdb.Server()
couch.resource.credentials = (username,password)
db = couch["wifi"]

#DBusGMainLoop(set_as_default=True)
#loop = gobject.MainLoop()
import NetworkManager
bus = dbus.SystemBus()
nm = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')

currentdev = None

for device in NetworkManager.NetworkManager.GetDevices():
    if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
        currentdev = device.SpecificDevice()
        break

def checkAccessPoints():
    if not currentdev == None:
        try:
            active = currentdev.ActiveAccessPoint
            access_points = currentdev.GetAccessPoints()
        except dbus.exceptions.DBusException:
            return
        for point in access_points:
            try:
                doc = db[point.Ssid]
            except couchdb.http.ResourceNotFound:
                doc = {}
            doc["_id"] = point.Ssid
            is_active = point.object_path == active.object_path
            n = datetime.datetime.now()
            #I'm using unix time bacause it makes it easy to do math
            unix_time = time.mktime(n.timetuple())
            if "time" in doc:
                doc["last_time"] = doc["time"]
            doc["time"] = unix_time
            doc["is_active"] = is_active
            doc["strength"] = int(point.proxy.Get(point.interface_name, "Strength",dbus_interface="org.freedesktop.DBus.Properties"))
            db.save(doc)
    #print "end"

while True:
    #print "begin"
    checkAccessPoints()
    time.sleep(5)

#I can't seem to get the interval loop working even the most simple
#example working on the gobject mainloop, there is no time to explore this
#further before I hand it in

#def handle_notification(state):
#    print wifi_states[int(state)]

#nm.connect_to_signal("StateChanged", handle_notification)

#gobject.timeout_add(5000, checkAccessPoints);
#loop.run()
