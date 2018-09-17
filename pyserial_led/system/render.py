import asyncio
import logging

from collections import deque

from pyserial_led.event.controller import ControllerEvent

from pyserial_led.mode.votesolid import VoteSolidMode
from pyserial_led.mode.rainbow import RainbowMode
from pyserial_led.mode.tothemoon import ToTheMoonMode
from pyserial_led.mode.snake import SnakeMode
from pyserial_led.mode.sparkle import SparkleMode


def get_event(event_queue):
    try:
        event = event_queue.get_nowait()
        return event
    except asyncio.QueueEmpty:
        return None


async def main(strips, event_queue):
    print("Starting up main task...")

    modes = [
        VoteSolidMode(),
        SnakeMode(strips[0].num_leds),
        SparkleMode(strips[0].num_leds),
        ToTheMoonMode(strips[0].num_leds),
        RainbowMode(),
    ]
    current_mode = 0
    num_strips = len(strips)

    while True :
        try:
            event = get_event(event_queue)
            if event is None:
                await asyncio.sleep(0)
                continue

            elif isinstance(event, ControllerEvent) and event.state == "press":
                if event.type == "select":
                    if current_mode >= len(modes) - 1:
                        current_mode = 0
                    else:
                        current_mode += 1
                    continue

            modes[current_mode].update(event)

            for s, strip in enumerate(strips):
                for i in range(strip.num_leds):
                    strip.set_pixel(i, modes[current_mode].render(i, s))

            [ strip.show() for strip in strips ]
            await asyncio.sleep(0)

        except Exception as e:
            logging.exception("Error in render!")
