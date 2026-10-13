# Rigol_controller

A Python/Tkinter GUI to control up to two Rigol bench power supplies (3 channels each) over USB, using PyVISA/SCPI.

## What the app does

- The **Find Power Supplies** menu command scans connected USB instruments and identifies any Rigol power supplies.
- Discovered supplies are listed in a combobox; pick one to connect.
- Each of the 3 channels has a Voltage entry, a Current entry, and an on/off button. Clicking the button sends the entered voltage/current to that channel and toggles its output; the button's label ("Turn Channel On"/"Turn Channel Off") always reflects the instrument's actual state and is refreshed automatically every 2 seconds.
- If a 2nd Rigol supply is found, a whole 2nd control panel is cloned to the right of the first and the window widens automatically, so each supply is controlled independently.

## Requirements

- Python 3.10+ (developed with 3.12)
- NI-VISA Runtime — provides the USB/VISA driver that `pyvisa` talks to (see below)

## Installation

1. Create and activate a virtual environment in the project folder:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install the Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Install NI-VISA

PyVISA itself is just a Python API — it needs a VISA backend installed on the PC to actually talk to the instrument over USB. NI-VISA is the recommended backend on Windows (free, no extra `pyusb`/driver juggling needed):

1. Download NI-VISA from NI's site:
   https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#607410
2. Run the installer and accept the defaults (the full "NI-VISA" package, not just the runtime-only option, is the safest choice). Reboot if the installer asks you to.
3. Plug the Rigol power supply in over USB. Windows should enumerate it as a VISA/USB Test and Measurement device, and `pyvisa.ResourceManager()` will find NI-VISA automatically — no further configuration needed.

NI-VISA is only required to control real hardware. You can try out the whole GUI without it using mock mode below.

## Running the app

- **Against real hardware:** double-click `test_gui.bat` (or run `.venv\Scripts\python.exe Rigol_Controller.py`).
- **Without any hardware (mock mode):** double-click `test_gui_mock.bat`. This simulates two Rigol supplies in memory so you can try the full UI — including the 2nd-panel duplication and the on/off workflow — without NI-VISA or any instrument connected. The window title shows "MOCK MODE" as a reminder.

Both `.bat` files keep their console window open after the GUI closes, so you can see any error output.

## Using the app

1. Menu → **Find Power Supplies**.
2. Pick a supply from each panel's combobox (hover over it to see the full identification string if it's cut off).
3. Enter a Voltage and Current for a channel, then click that channel's button to apply the values and turn the output on. Click again to turn it off.

## Saving and reloading settings

- **Save Settings** (menu): saves the Voltage/Current currently typed into each connected panel's 3 channels to a JSON file you choose. Settings are keyed by the supply's `*IDN?` string, not its USB port, so they still match after reconnecting via a different cable/port.
- **Load Settings** (menu): pick a previously saved JSON file; for each panel with a supply currently selected, its matching saved values (by IDN) are filled into that panel's Voltage/Current entry boxes.
- Loading only fills in the entry boxes — it does **not** write to the instrument or change outputs. Click each channel's button afterwards to apply the values and turn it on, same as always.
- A panel with no supply selected (or no matching IDN in the file) is just skipped; a summary popup reports how many channels were saved/loaded.
