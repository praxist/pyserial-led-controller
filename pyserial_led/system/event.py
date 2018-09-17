import evdev
import asyncio
from pyserial_led.event.timetick import TimeTickEvent
from pyserial_led.event.controller import ControllerEvent


async def timetick(event_queue):
    while True:
        await asyncio.sleep(0.01)
        try:
            event_queue.put_nowait(TimeTickEvent())
        except asyncio.QueueFull:
            print("Could not enqueue a timetick because the queue is full!!")


async def controller(gamepad, event_queue):
    while True:
        print("Starting up controller-reader coroutine...")
        async for event in gamepad.async_read_loop():
            if event.type in [evdev.ecodes.EV_KEY, evdev.ecodes.EV_ABS]:
                try:
                    event_queue.put_nowait(ControllerEvent(event))
                except asyncio.QueueFull:
                    print("Queue is full, ignoring event {0}".format(ControllerEvent(event)))
        await asyncio.sleep(0.2)
