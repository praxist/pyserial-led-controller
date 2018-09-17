from pyserial_led.util.color import Color
from pyserial_led.event.controller import ControllerEvent
from pyserial_led.event.timetick import TimeTickEvent


class RainbowMode():
    def __init__(self):
        self.elapsed = 0
        self.max = 500
        self.speed = 3
        self.spacing = 4


    def update(self, event):
        if isinstance(event, TimeTickEvent):
            if self.elapsed == self.max:
                self.elapsed = 0
            else:
                self.elapsed += 1

        elif isinstance(event, ControllerEvent):
            if event.type == "r":
                self.speed = self.speed + 1 if self.speed < 10 else 10
            elif event.type == "l":
                self.speed = self.speed - 1 if self.speed > 1 else 1
            elif event.type == "left":
                self.spacing = self.spacing + 1 if self.spacing < 20 else 20
            elif event.type == "right":
                self.spacing = self.spacing - 1 if self.spacing > 1 else 1


    def render(self, pos, strip):
        return Color.hsv((self.elapsed * self.speed + pos * self.spacing) %
                         500 / 500.0, 1, 0.5)
