import serial
from time import sleep
from functools import reduce


class Strip:
    def __init__(self, device, num_leds, code):
        self.num_leds = num_leds
        self.leds = [bytearray([0, 0, 0])] * num_leds
        self.code = bytearray(code.encode())
        self.ser = serial.Serial(device, 500000)

        sleep(0.5)
        self.show()

    def wipe(self):
        for i in range(self.num_leds):
            self.set_pixel(i, [0] * 3)
        self.show()


    def set_pixel(self, pos, rgb):
        self.leds[pos] = bytearray([rgb[0], rgb[1], rgb[2]])


    def show(self):
        self.ser.write(self.code + reduce((lambda x, y: x + y), self.leds))

