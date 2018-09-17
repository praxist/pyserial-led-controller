import serial
import evdev
import asyncio

import pyserial_led.util as util
import pyserial_led.system as sys
import pyserial_led.layout as layout


if __name__ == "__main__":
    gamepad = evdev.InputDevice('/dev/input/event0')
    num_leds = 129
    arduino_port = util.find_port()

    strip_up = layout.Strip(arduino_port, num_leds, 'A')
    strip_down = layout.Strip(arduino_port, num_leds, 'B')

    loop = asyncio.get_event_loop()
    try:
        event_queue = asyncio.Queue(10)

        asyncio.ensure_future(sys.render.main((strip_up, strip_down), event_queue)),
        asyncio.ensure_future(sys.event.controller(gamepad, event_queue))
        asyncio.ensure_future(sys.event.timetick(event_queue))

        loop.run_forever()
    finally:
        loop.close()
        strip_up.wipe()
        strip_down.wipe()
