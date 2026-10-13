#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Discovery of Rigol power supplies among the available USB VISA resources."""


def find_rigol_supplies(resource_manager):
    """Return a list of (resource_name, idn_string) for connected Rigol gear.

    Opens each USB VISA resource briefly to query *IDN?, keeps the ones that
    identify as Rigol, and closes them again (the caller reconnects to
    whichever one the user selects).
    """
    found = []
    for resource_name in resource_manager.list_resources():
        if not resource_name.startswith('USB'):
            continue
        try:
            instrument = resource_manager.open_resource(resource_name)
            instrument.timeout = 2000
            instrument.read_termination = '\n'
            instrument.write_termination = '\n'
            idn = instrument.query('*IDN?').strip()
            instrument.close()
        except Exception:
            continue
        if 'RIGOL' in idn.upper():
            found.append((resource_name, idn))
    return found
