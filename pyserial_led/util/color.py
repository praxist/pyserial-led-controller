from colorsys import hsv_to_rgb


class Color:
    BLUE = [0, 0, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    WHITE = [255] * 3
    BLACK = [0] * 3
    ORANGEY = [255, 68, 0]
    BLUEY = [0, 120, 210]


    @staticmethod
    def hsv(h, s, v):
        return list(map(lambda x: int(round(x * 255)), hsv_to_rgb(h, s, v)))


