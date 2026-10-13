#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""PyVISA wrapper for a Rigol DP8xx-style, 3-channel bench power supply."""

import threading


class RigolPSU:
    """One connected Rigol power supply, addressed by VISA resource string."""

    def __init__(self, resource_manager, resource_name):
        self.resource_manager = resource_manager
        self.resource_name = resource_name
        self.instrument = None
        self.idn = None
        self._lock = threading.Lock()

    def connect(self):
        self.instrument = self.resource_manager.open_resource(self.resource_name)
        self.instrument.timeout = 5000
        self.instrument.read_termination = '\n'
        self.instrument.write_termination = '\n'
        self.idn = self.instrument.query('*IDN?').strip()
        return self.idn

    def select_channel(self, channel):
        self.instrument.write(f':INST CH{channel}')

    def set_voltage(self, channel, volts):
        with self._lock:
            self.select_channel(channel)
            self.instrument.write(f':VOLT {volts}')

    def set_current(self, channel, amps):
        with self._lock:
            self.select_channel(channel)
            self.instrument.write(f':CURR {amps}')

    def set_output(self, channel, on):
        state = 'ON' if on else 'OFF'
        with self._lock:
            self.instrument.write(f':OUTP CH{channel},{state}')

    def is_output_on(self, channel):
        with self._lock:
            reply = self.instrument.query(f':OUTP? CH{channel}')
        return reply.strip().upper() == 'ON'

    def close(self):
        if self.instrument is not None:
            try:
                self.instrument.close()
            finally:
                self.instrument = None
