from app.indicator import Indicator
from app.backends.upower import UPowerBackend
from gi.repository import GLib

def start():
    backend = UPowerBackend()
    indicator = Indicator(backend)
    GLib.MainLoop().run()
