from typing import Callable, Any
from app.indicator import Status
from app.backends.interface import BackendInterface
from pyudev import Context, Monitor, MonitorObserver, Device
from gi.repository import GLib
import time
from threading import Timer

class UDevBackend(BackendInterface):

    def __init__(self):
        self.context = Context()
        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by('power_supply')

        self.percent_callback = None
        self.status_callback = None

        (self.battery, self.line_power) = self.find_devices()

        if not self.battery:
            raise BatteryNotFoundError()

        if not self.line_power:
            raise LinePowerNotFoundError()

        self.last_percent = -1
        self.last_status = None

        def on_udev_event(device):
            if device == self.battery:
                self.battery = device
                percent = self.get_percent()
                if percent != self.last_percent:
                    self.last_percent = percent
                    if self.percent_callback:
                        GLib.idle_add(self.percent_callback, percent)

            elif device == self.line_power:
                self.line_power = device
                status = self.get_status()
                if status != self.last_status:
                    self.last_status = status
                    if self.status_callback:
                        GLib.idle_add(self.status_callback, status)


        # XXX I can't get udev (or acpi) to give me battery discharge events
        # without requiring system configuration so we have to poll
        interval = 20000
        def poll_udev():
            battery = Device.from_path(self.context, self.battery.device_path)
            on_udev_event(battery)
            GLib.timeout_add(interval, poll_udev)

        GLib.timeout_add(interval, poll_udev)

        self.observer = MonitorObserver(self.monitor, callback=on_udev_event)

        self.observer.start()


    def find_devices(self):
        line_power = None
        battery = None

        for device in self.context.list_devices(subsystem='power_supply'):
            device_type = device.attributes.asstring('type').lower()
            # TODO
            # 1. handle empty battery port
            # 2. handle multiple devices
            if device_type == 'battery':
                battery = device
            elif device_type == 'mains':
                line_power = device

        return (battery, line_power)


    def get_status(self) -> Status:
        is_online = int(self.line_power.attributes.get('online')) == 1
        if is_online:
            return Status.CHARGING
        else:
            return Status.DISCHARGING


    def get_percent(self) -> float:
        return float(self.battery.attributes.get('capacity'))


    def on_status_change(self, fn: Callable[[Status], None]) -> None:
        self.status_callback = fn


    def on_percent_change(self, fn: Callable[[float], None]) -> None:
        self.percent_callback = fn
