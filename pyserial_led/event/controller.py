import evdev


class ControllerEvent:
    KEYMAPPINGS_DIRECTIONS = {
        (1, 0):   "up",
        (1, 127): "neutral",
        (1, 255): "down",
        (0, 0):   "left",
        (0, 127): "neutral",
        (0, 255): "right",
    }
    KEYMAPPINGS_BUTTONS = {
        (305, 0): "a-up",
        (305, 1): "a",
        (306, 0): "b-up",
        (306, 1): "b",
        (304, 0): "x-up",
        (304, 1): "x",
        (307, 0): "y-up",
        (307, 1): "y",
        (312, 0): "select-up",
        (312, 1): "select",
        (313, 0): "start-up",
        (313, 1): "start",
        (309, 0): "r-up",
        (309, 1): "r",
        (308, 0): "l-up",
        (308, 1): "l",
    }


    def __init__(self, event):

        if event.type == evdev.ecodes.EV_ABS:
            self.type = self.KEYMAPPINGS_DIRECTIONS[(event.code, event.value)]
            if "neutral" in self.type:
                self.state = "release"
            else:
                self.state = "press"
        elif event.type == evdev.ecodes.EV_KEY:
            self.type = self.KEYMAPPINGS_BUTTONS[(event.code, event.value)]
            if "up" in self.type:
                self.state = "release"
            else:
                self.state = "press"
        else:
            self.type = None
            self.state = None

        self.key = event.code
        self.value = event.value


    def __str__(self):
        return ("-------EVENT-------\n" +
            "Key: {0}\n".format(self.key) +
            "Value: {0}\n".format(self.value) +
            "Type: {0}\n".format(self.type))
