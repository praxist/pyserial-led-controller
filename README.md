# pyserial-led-controller

Controls LED strips using a microcontroller and a Raspberry Pi using the pyserial python library.

Currently this code is in use to drive two WS2811 strips with a Raspberry Pi 3 B+.

## Usage
To use, copy this repo and make the following modifications:

- modify controller.ino and change the macros and FastLED init code to support whatever strip you'll be running
- dump new LED patterns into the mode directory
- render.py contains the list of modes that will be displayed
