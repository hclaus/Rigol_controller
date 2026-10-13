#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Data model for persisting per-channel set-points to a JSON file.

Keyed by instrument IDN (not VISA resource string) so saved values still
apply after reconnecting to a different USB port. Menu wiring for Save/Load
Settings is a follow-up phase; this just defines the format and I/O.

File format:
{
    "<idn string>": {
        "1": {"voltage": 3.3, "current": 1.0},
        "2": {"voltage": 5.0, "current": 0.5},
        "3": {"voltage": 12.0, "current": 0.2}
    }
}
"""

import json


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_channel_settings(data, idn, channel):
    return data.get(idn, {}).get(str(channel))


def set_channel_settings(data, idn, channel, voltage, current):
    data.setdefault(idn, {})[str(channel)] = {'voltage': voltage, 'current': current}
