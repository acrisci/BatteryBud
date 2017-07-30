from pyudev import Context, Monitor, MonitorObserver

context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by('power_supply')

battery = None
line_power = None

def is_device_battery(device):
    try:
        if device.attributes.asstring('type').lower() == 'battery':
            return True
    except KeyError:
        pass

    return False

def is_device_line_power(device):
    try:
        if device.attributes.asstring('type').lower() == 'mains':
            return True
    except KeyError:
        pass

    return False


for d in context.list_devices(subsystem='power_supply'):
    print(d)
    if is_device_battery(d):
        battery = d
    if is_device_line_power(d):
        line_power = d
    print('properties:')
    for p in d.properties:
        print('{}: {}'.format(p, d.get(p)))
    print('attributes:')
    for a in d.attributes.available_attributes:
        print('{}: {}'.format(a, d.attributes.get(a)))

def on_device_event(device):
    if device == battery:
        battery = device
        print('got a battery event')
    elif device == line_power:
        line_power = device
        print('got a line power event')

observer = MonitorObserver(monitor, callback=on_device_event, name='monitor-observer')

#observer.start()
