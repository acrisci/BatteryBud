from app.indicator import Indicator
from app.backends.upower import UPowerBackend
from gi.repository import GLib

def start():
    indicator = Indicator()
    backend = UPowerBackend(indicator)
    GLib.MainLoop().run()
