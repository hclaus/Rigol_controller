#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""In-memory stand-ins for RigolPSU/discovery, for UI testing without hardware.

Enabled by setting the RIGOL_MOCK=1 environment variable before launching
the app (see test_gui_mock.bat). Reports two fake Rigol supplies so the
panel-duplication path can be exercised, and simulates voltage/current/
output state per channel in memory instead of talking to real hardware.
"""


def find_mock_supplies():
    return [
        ('MOCK0::DP832::A::INSTR', 'RIGOL TECHNOLOGIES,DP832,MOCK0000000001,00.00.00 (MOCK)'),
        ('MOCK0::DP832::B::INSTR', 'RIGOL TECHNOLOGIES,DP832,MOCK0000000002,00.00.00 (MOCK)'),
    ]


class MockRigolPSU:
    def __init__(self, resource_manager, resource_name):
        self.resource_manager = resource_manager
        self.resource_name = resource_name
        self.idn = None
        self._state = {ch: {'voltage': 0.0, 'current': 0.0, 'on': False} for ch in (1, 2, 3)}

    def connect(self):
        self.idn = f'MOCK supply at {self.resource_name}'
        return self.idn

    def select_channel(self, channel):
        pass

    def set_voltage(self, channel, volts):
        self._state[channel]['voltage'] = volts

    def set_current(self, channel, amps):
        self._state[channel]['current'] = amps

    def set_output(self, channel, on):
        self._state[channel]['on'] = on

    def is_output_on(self, channel):
        return self._state[channel]['on']

    def close(self):
        pass
