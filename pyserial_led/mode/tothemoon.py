from pyserial_led.util.color import Color
from pyserial_led.event.controller import ControllerEvent
from pyserial_led.event.timetick import TimeTickEvent
import math


class ToTheMoonMode:
    def __init__(self, num_leds):
        self.elapsed = 0
        self.time_to_update = 1

        self.num_leds = num_leds
        self.sink = math.ceil(num_leds / 2)
        self.doot_size = 6
        self.updoots = set()
        self.downdoots = set()


    def update(self, event):
        if isinstance(event, TimeTickEvent):
            if self.elapsed >= self.time_to_update - 1:
                self.elapsed = 0

                self.updoots = set(map(lambda x: x + 1, self.updoots))
                self.updoots.discard(self.sink)

                self.downdoots = set(map(lambda x: x + 1, self.downdoots))
                self.downdoots.discard(self.sink)
            else:
                self.elapsed += 1


        elif isinstance(event, ControllerEvent):
            if event.type == "up":
                self.updoots.add(0)
            elif event.type == "down":
                self.downdoots.add(0)
            elif event.type == "right":
                self.doot_size = self.doot_size + 1 if self.doot_size < 10 else 10
            elif event.type == "left":
                self.doot_size = self.doot_size - 1 if self.doot_size > 1 else 1
            elif event.type == "l":
                self.time_to_update = self.time_to_update + 1 if self.time_to_update < 10 else 10
            elif event.type == "r":
                self.time_to_update = self.time_to_update - 1 if self.time_to_update > 1 else 1


    def render(self, pos, strip):
        if pos < self.sink:
            valid_positions = set(max(pos - x, 0) for x in range(0, self.doot_size))
            if strip == 0 and not valid_positions.isdisjoint(self.updoots):
                return Color.ORANGEY
            elif strip == 1 and not valid_positions.isdisjoint(self.downdoots):
                return Color.BLUEY
            else:
                return Color.BLACK
        else:
            valid_positions = set(min(self.num_leds - pos + x,
                                      self.num_leds) for x in range(0, self.doot_size))
            if strip == 0 and not valid_positions.isdisjoint(self.updoots):
                return Color.ORANGEY
            elif strip == 1 and not valid_positions.isdisjoint(self.downdoots):
                return Color.BLUEY
            else:
                return Color.BLACK
