from app.indicator import Indicator
from app.backends.upower import UPowerBackend, BatteryNotFoundError, LinePowerNotFoundError
from gi.repository import GLib

def start():
    try:
        backend = UPowerBackend()
        indicator = Indicator(backend)
        GLib.MainLoop().run()
        return 0
    except BatteryNotFoundError:
        print('ERROR: could not find a battery')
        return 1
    except LinePowerNotFoundError:
        print('ERROR: could not find line power device')
        return 1
