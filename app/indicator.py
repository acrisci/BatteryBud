#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
import os
from enum import Enum, unique
import math
import textwrap


class Status(Enum):
    CHARGING = 1
    DISCHARGING = 2
    ALERT = 3
    UNKNOWN = 4

    def to_human_readable(self):
        lookup = {
            Status.CHARGING: 'Plugged in',
            Status.DISCHARGING: 'Discharging',
            Status.ALERT: 'Alert!',
            Status.UNKNOWN: 'Unknown status',
        }
        return lookup[self]


@unique
class Color(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Indicator(Gtk.StatusIcon):

    def __init__(self, backend):
        super().__init__()

        self.backend = backend
        self.icon_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'icons')
        self.percent = backend.get_percent()
        self.status = backend.get_status()
        self.color = Color.WHITE

        def percent_handler(percent):
            self.percent = percent
            self.update()

        def status_handler(status):
            self.status = status
            self.update()

        backend.on_status_change(status_handler)
        backend.on_percent_change(percent_handler)

        self.update()


    @staticmethod
    def iconic_percent(percent):
        choices = [20, 30, 50, 60, 80, 90, 100]
        ipercent = 100
        delta = 999999

        for idx,c in enumerate(choices):
            new_delta = abs(c - percent)
            if new_delta < delta:
                delta = new_delta
                ipercent = choices[idx]

        return str(ipercent)


    def icon_path(self):
        beginning = ['ic', 'battery']
        ending = [str(self.color.value), '48dp']

        if self.status in [ Status.ALERT, Status.UNKNOWN ]:
            if self.status is Status.ALERT:
                beginning.append('alert')
            elif self.status is Status.UNKNOWN:
                beginning.append('unknown')
        else:
            if self.status is Status.CHARGING:
                beginning.append('charging')

            ipercent = Indicator.iconic_percent(self.percent)
            if ipercent == '100':
                ipercent = 'full'

            beginning.append(ipercent)

        return os.path.join(
                self.icon_dir,
                '_'.join(beginning + ending) + '.png')


    def update(self):
        template = {
            'charging': self.status.to_human_readable(),
            'percent': str(self.percent)
        }
        fmt = textwrap.dedent('''
        {percent}%
        {charging}
        ''').strip()
        self.props.tooltip_text = fmt.format(**template)
        self.props.file = self.icon_path()
