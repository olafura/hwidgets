import dbus
import json
from PySide.QtCore import QObject, Slot, Signal

class Battery(QObject):

    def __init__(self):
        super(Battery, self).__init__()
        self.bus = dbus.SystemBus()
        self.upower = self.bus.get_object("org.freedesktop.UPower","/org/freedesktop/UPower/devices/battery_BAT0")
        self.upower_i = dbus.Interface(self.upower,dbus_interface="org.freedesktop.DBus.Properties")

    @Slot(str)
    def getCurrentBattery(self, value):
        properties = self.upower_i.GetAll("org.freedesktop.UPower.Device")
        # I have to go through the properties because the json encoder does not
        # support dbus.Double as a conversion unit
        for key, value in properties.items():
                if isinstance(value, dbus.Double):
                    properties[key] = float(value)

        self.on_battery_status.emit(json.dumps(properties))

    on_battery_status = Signal(str)

#@Slot(str)
#def printBattery(value):
#    print(value)
#
#battery = Battery()
#battery.on_battery_status.connect(printBattery)
#battery.getCurrentBattery()
