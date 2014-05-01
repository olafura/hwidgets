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
nm = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')

for device in NetworkManager.NetworkManager.GetDevices():
    if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
        dev = device.SpecificDevice()
        active = dev.ActiveAccessPoint
        access_points = dev.GetAccessPoints()
        for point in access_points:
            try:
                doc = db[point.Ssid]
            except couchdb.http.ResourceNotFound:
                doc = {}
            doc["_id"] = point.Ssid
            is_active = point.object_path == active.object_path
            n = datetime.datetime.now()
            unix_time = time.mktime(n.timetuple())
            if "time" in doc:
                doc["last_time"] = doc["time"]
            doc["time"] = unix_time
            doc["is_active"] = is_active
            doc["strength"] = int(point.proxy.Get(point.interface_name, "Strength",dbus_interface="org.freedesktop.DBus.Properties"))
            db.save(doc)

def handle_notification(state):
    print wifi_states[int(state)]
nm.connect_to_signal("StateChanged", handle_notification)
loop.run()
