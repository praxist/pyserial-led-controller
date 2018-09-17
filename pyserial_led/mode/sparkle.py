from pyserial_led.util.color import Color
from pyserial_led.event.controller import ControllerEvent
from pyserial_led.event.timetick import TimeTickEvent
from random import random
import math


class SparkleMode():
    def __init__(self, num_leds):
        self.elapsed = 0
        self.end = 2

        self.sparkles = {}
        self.spacing = 5
        self.max_sparkles = 10
        self.num_leds = num_leds
        self.sparkle_variance = 0.5


    def update(self, event):
        if isinstance(event, TimeTickEvent):
            if self.elapsed >= self.end - 1:
                self.elapsed = 0

                self.sparkles = { pos : sparkle for pos, sparkle in self.sparkles.items() if
                 not sparkle.fade() }

                if len(self.sparkles) <= self.max_sparkles and random() < 0.3:
                    potential_pos = int(random() * self.num_leds)

                    # UGLY and very likely not working properly
                    valid_pos = True
                    for pos in [ i + potential_pos for i in range(0, self.spacing)]:
                        if pos in self.sparkles:
                            valid_pos = False
                            break

                    if valid_pos:
                        self.sparkles[potential_pos] = Sparkle(1 - random() * self.sparkle_variance)

            else:
                self.elapsed += 1



    def render(self, pos, strip):
        if pos in self.sparkles:
            if strip == 0:
                return Color.hsv(0.0451, 1, self.sparkles[pos].brightness())
            elif strip == 1:
                return Color.hsv(0.5711, 1, self.sparkles[pos].brightness())
            else:
                return Color.BLACK
        else:
            return Color.BLACK



class Sparkle:
    def __init__(self, brightness_factor):
        self.brightness_factor = brightness_factor
        self.lifespan = 40
        self.age = 1


    def fade(self):
        self.age += 1
        return self.age >= self.lifespan - 1


    def brightness(self):
        return math.sin(math.pi * float(self.age) / self.lifespan ) * self.brightness_factor


