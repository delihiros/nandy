import bit

class Screen:
    def __init__(self):
        size = 32 * 256
        self._memory = [0] * size

    def invoke(self, in16, load, address13):
        if load == 0:
            return self._memory[address13]
        else:
            self._memory[address13] = in16


class Keyboard:
    def __init__(self):
        self._memory = 0

    def invoke(self):
        return 0


class Memory:
    def __init__(self):
        size = 0x6000
        self._memory = [0] * size
        self.screen = Screen()
        self.keyboard = Keyboard()

    def invoke(self, in16, load, address15):
        if address15 > size:
            return
        elif 0x4000 <= address15 and address15 <= 0x5FFF:
            address13 = bit.extract(address15, 0, 12)
            return self.screen.invoke(in16, load, address13)
        elif address15 == 0x6000:
            return self.keyboard.invoke()
        elif load == 0:
            return self._memory[address15]
        else:
            self._memory[address15] = in16
