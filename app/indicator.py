#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
import os
from enum import Enum, auto, unique
import math


class Status(Enum):
    CHARGING = auto()
    DISCHARGING = auto()
    ALERT = auto()
    UNKNOWN = auto()


@unique
class Color(Enum):
    WHITE = 'white'
    BLACK = 'black'


class Indicator(Gtk.StatusIcon):

    def __init__(self):
        self.icon_dir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'icons')
        self.percent = 100
        self.status = Status.DISCHARGING
        self.color = Color.WHITE
        super().__init__()


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
        self.props.file = self.icon_path()
