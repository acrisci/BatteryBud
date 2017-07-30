from app.indicator import Indicator
from app.backends.interface import BatteryNotFoundError, LinePowerNotFoundError
from app.backends.upower import UPowerBackend
from app.backends.udev import UDevBackend
from gi.repository import GLib

class NoBatteryBackendError(Exception):
    pass

def get_backend():
    # TODO improve error handling
    backend = None
    last_error = None

    try:
        backend = UPowerBackend()
    except Exception as e:
        # TODO log
        last_error = e

    try:
        backend = UDevBackend()
    except Exception:
        # TODO log
        last_error = e

    if not backend:
        raise NoBatteryBackendError(last_error)

    return backend

def start():
    try:
        main_loop = GLib.MainLoop()
        backend = get_backend()
        indicator = Indicator(backend)
        main_loop.run()
        return 0
    except BatteryNotFoundError:
        print('ERROR: could not find a battery')
        return 1
    except LinePowerNotFoundError:
        print('ERROR: could not find line power device')
        return 1
