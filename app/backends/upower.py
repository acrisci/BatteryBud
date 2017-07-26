from gi.repository import GLib
import dbus
import dbus.mainloop.glib
import sys
from enum import Enum
from app.indicator import Status
from app.backends.interface import BackendInterface

# https://upower.freedesktop.org/docs/Device.html#Device:State
class UPowerState(Enum):
    UNKNOWN = 0
    CHARGING = 1
    DISCHARGING = 2
    EMPTY = 3
    FULLY_CHARGED = 4
    PENDING_CHARGE = 5
    PENDING_DISCHARGE = 6


    def to_indicator_status(self):
        if self is UPowerState.UNKNOWN:
            return Status.UNKNOWN
        if self in [UPowerState.CHARGING,
                    UPowerState.PENDING_CHARGE,
                    UPowerState.FULLY_CHARGED]:
            return Status.CHARGING
        else:
            return Status.DISCHARGING


# https://upower.freedesktop.org/docs/Device.html#Device:Type
class UPowerType(Enum):
    UNKNOWN = 0
    LINE_POWER = 1
    BATTERY = 2
    UPS = 3
    MONITOR = 4
    MOUSE = 5
    KEYBOARD = 6
    PDA = 7
    PHONE = 8


class Device:
    def __init__(self, bus, dbus_path):
        self.object = bus.get_object('org.freedesktop.UPower',
                dbus_path)
        self.properties = dbus.Interface(self.object,
                'org.freedesktop.DBus.Properties')
        self.device = dbus.Interface(self.object,
                'org.freedesktop.UPower.Device')


    def get_property(self, prop):
        return self.properties.Get('org.freedesktop.UPower.Device', prop)

    
    def get_type(self):
        upower_type = self.get_property('Type')
        return UPowerType(upower_type)


    def get_percentage(self):
        percentage = self.get_property('Percentage')
        return percentage


    def get_state(self):
        upower_state = self.get_property('State')
        return UPowerState(upower_state)


    def refresh(self):
        self.device.Refresh()


class UPowerBackend(BackendInterface):
    def find_devices(self):
        upower = self.system_bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower')
        devices = upower.EnumerateDevices(dbus_interface='org.freedesktop.UPower')

        battery = None
        line_power = None

        for device_path in devices:
            device = Device(self.system_bus, device_path)
            upower_type = device.get_type()

            # TODO
            # 1. handle empty battery port
            # 2. handle multiple devices
            if upower_type is UPowerType.BATTERY:
                battery = device
            elif upower_type is UPowerType.LINE_POWER:
                line_power = device

        return (battery, line_power)


    def __init__(self, indicator):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.indicator = indicator
        self.system_bus = dbus.SystemBus()
        (self.battery, self.line_power) = self.find_devices()

        if not self.battery:
            raise Exception('could not find a battery')

        if not self.line_power:
            raise Exception('could not find a line power device')

        self.battery.refresh()
        indicator.status = self.battery.get_state().to_indicator_status()
        indicator.percent = self.battery.get_percentage()

        def battery_signal_handler(iface, props, _):
            if 'Percentage' in props:
                indicator.percent = props['Percentage']
                indicator.update()

        def line_power_signal_handler(iface, props, _):
            if 'Online' in props:

                if props['Online']:
                    indicator.status = Status.CHARGING
                else:
                    indicator.status = Status.DISCHARGING

                indicator.update()


        self.battery.properties.connect_to_signal('PropertiesChanged', battery_signal_handler)
        self.line_power.properties.connect_to_signal('PropertiesChanged', line_power_signal_handler)

        indicator.update()
