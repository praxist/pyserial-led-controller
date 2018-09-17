from pyserial_led.util.color import Color
from pyserial_led.event.controller import ControllerEvent


class VoteSolidMode:
    def __init__(self):
        self.colors = [Color.BLUEY, Color.ORANGEY]
        self.switch = 1


    def update(self, event):
        if isinstance(event, ControllerEvent):
            if event.type == "up":
                self.switch = 1
            elif event.type == "down":
                self.switch = 0


    def render(self, pos, strip):
        if strip == 0:
            return self.colors[self.switch]
        elif strip == 1:
            return self.colors[self.switch ^ 1]

