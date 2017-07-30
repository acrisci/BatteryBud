BatteryBud
==========

A standalone battery power indicator tray icon.

About
-----

*BatteryBud is in the early phases of development. Please report bugs and feature requests on GitHub.*

BatteryBud is a battery power indicator. It sits in your system tray and displays a little icon that tells you if your laptop is charging or needs to be charged.

BatteryBud currently depends on either `udev <https://en.wikipedia.org/wiki/Udev>`__ or the `UPower Device DBus Specification <https://upower.freedesktop.org/docs/Device.html>`__ but other backends will be supported in the future upon request. It should work on all up to date Linux desktop systems.


Usage
-----

BatteryBud requires Python 3, `PyGObject <https://pygobject.readthedocs.io/en/latest/>`__, `dbus-python <https://www.freedesktop.org/wiki/Software/DBusBindings/>`__, and `pyudev <https://pyudev.readthedocs.io/en/latest/index.html>`__ to run.

```
# ArchLinux
pacman -S python-gobject python-dbus gtk3 dbus-glib python-pyudev
```

Simply run `./batterybud` to start the app and you should see a battery indicator in your tray (if you have a battery on your system).

TODO
----

Right now, it just shows an icon that indicates how charged the battery is and whether or not it is charging but more work is planned.

* Support more backends to get battery status (currently supports udev and UPower)
* Hover tooltip that shows time remaining on the battery charge
* Display detailed battery info
* Change the color/appearance of the icon
* Logging
* Expose functions to CLI
* Text and gui configuration
* Make dbus dependencies optional

Contributing
------------

Contributions are welcome for this project. Please report bugs, write documentation, and request features on GitHub.

License
-------

This work is available under a FreeBSD License (see LICENSE).

Copyright © 2017, Tony Crisci

All rights reserved.
