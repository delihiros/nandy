class ROM32K:
    def __init__(self):
        self.size = 32000
        self._memory = [0] * self.size

    def load_rom(self, rom_file):
        # pretend that the rom_file contains 16 bit op per line as a digit such as 0101010101010101
        with open(rom_file, 'r') as f:
            for idx, b in enumerate(f):
                self._memory[idx] = int(b, 2)

    def invoke(self, address15):
        return self._memory[address15]
