import gobject
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import json
DBusGMainLoop(set_as_default=True)
import NetworkManager
from mapping import wifi_states
from PySide.QtCore import QObject, Slot, Signal

#A simple class simulate simulate the access point information
class AP(object):
    Ssid = ""
    object_path = ""

    def __init__(self, Ssid, object_path):
        self.Ssid = Ssid
        self.object_path = object_path

class Wifi(QObject):

    def __init__(self):
        super(Wifi, self).__init__()
        self.loop = gobject.MainLoop()
        self.bus = dbus.SystemBus()

        self.currentdev = None
        #I have to keep track of the access points because dbus deletes the
        #information
        self.current_access_points = {}

        for device in NetworkManager.NetworkManager.GetDevices():
            if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
                self.currentdev = device.SpecificDevice()
                break
        self.currentdev.connect_to_signal("AccessPointAdded", self.handle_apadded)
        self.currentdev.connect_to_signal("AccessPointRemoved", self.handle_apremove)

    def getAP(self, point, active_op, available):
            #print("point op", str(point.object_path))
            #print("active op", str(active_op))
            doc = {}
            doc["ssid"] = point.Ssid
            is_active = str(point.object_path) == str(active_op)
            doc["is_available"] = available
            doc["is_active"] = is_active
            if available:
                new_ap = AP(str(point.Ssid),str(point.object_path))
                self.current_access_points[point.object_path] = new_ap
                doc["strength"] = int(point.proxy.Get(point.interface_name, "Strength",dbus_interface="org.freedesktop.DBus.Properties"))
            else:
                doc["strength"] = 0
            return doc


    @Slot(str)
    def checkAccessPoints(self,value):
        if not self.currentdev == None:
            try:
                active = self.currentdev.ActiveAccessPoint
                access_points = self.currentdev.GetAccessPoints()
            except dbus.exceptions.DBusException:
                return
            active_op = active.object_path
            ap_docs = []
            for point in access_points:
                doc = self.getAP(point, active_op, True)
                ap_docs.append(doc)
            #I use bulk update so I spend less time updating the access points
            #and less events
            #db.update(ap_docs)
        #print "end"
        self.on_wifi_status.emit(json.dumps(ap_docs))


    def handle_apadded(self, ap):
        #print("new_ap")
        #print("ap", ap)
        active = self.currentdev.ActiveAccessPoint
        active_op = active.object_path
        doc = self.getAP(ap, active_op, True)
        self.on_wifi_status.emit(json.dumps([doc]))
        #db.save(doc)
        #print ap

    def handle_apremove(self, ap):
        #print("delete_ap")
        #print("ap", ap)
        new_ap = self.current_access_points[ap.object_path]
        #by defination a deleted access_point can't be the current accesspoint
        #that's why I pass False as the second argument
        doc = self.getAP(new_ap, False, False)
        self.on_wifi_status.emit(json.dumps([doc]))
        #print("doc",doc)
        #db.save(doc)

    on_wifi_status = Signal(str)
#checkAccessPoints()


#@Slot(str)
#def printWifi(value):
#    print("printWifi")
#    print(value)

#wifi = Wifi()
#wifi.on_wifi_status.connect(printWifi)
#wifi.checkAccessPoints()
#wifi.loop.run()
