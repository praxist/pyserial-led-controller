from pyserial_led.util.color import Color
from pyserial_led.event.controller import ControllerEvent
from pyserial_led.event.timetick import TimeTickEvent


class SnakeMode:
    def __init__(self, num_leds):
        self.update_counter = 0
        self.time_to_update = 2

        self.add_dot_interval = 10
        self.dot_counter = 0

        self.elapsed = 0
        self.num_leds = num_leds
        self.dot_size = 6
        self.dots_up = set()
        self.dots_down = set()


    def update(self, event):
        if isinstance(event, TimeTickEvent):
            if self.update_counter >= self.time_to_update:
                self.update_counter = 0
                if self.dot_counter >= self.add_dot_interval:
                    self.dots_up.add(self.elapsed)
                    self.dot_counter = 0


                if self.elapsed == self.num_leds - 1:
                    self.elapsed = 0
                else:
                    self.elapsed += 1
                    self.dot_counter += 1

                self.dots_up.discard(self.elapsed)

            else:
                self.update_counter += 1


        elif isinstance(event, ControllerEvent):
            if event.type == "up":
                self.dots_up.add(self.elapsed)
            elif event.type == "down":
                self.dots_down.add(self.elapsed)
            elif event.type == "right":
                self.dot_size = self.dot_size + 1 if self.dot_size < 10 else 10
            elif event.type == "left":
                self.dot_size = self.dot_size - 1 if self.dot_size > 1 else 1
            elif event.type == "l":
                self.time_to_update = self.time_to_update + 1 if self.time_to_update < 10 else 10
            elif event.type == "r":
                self.time_to_update = self.time_to_update - 1 if self.time_to_update > 1 else 1


    def render(self, pos, strip):
        valid_positions = set([ (self.elapsed - max(pos - t, 0)) % self.num_leds
                               for t in range(self.dot_size) ])

        if not set(valid_positions).isdisjoint(self.dots_up):
            if strip == 0:
                return Color.ORANGEY
            elif strip == 1:
                return Color.BLUEY
            else:
                return Color.BLACK
        else:
            return Color.BLACK


