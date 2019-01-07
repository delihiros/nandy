class Bus:
    def __init__(self, rom, memory):
        self.rom = rom
        self.memory = memory

    def read_rom(self, address):
        return self.rom.invoke(address)

    def read(self, address15):
        return self.memory.invoke(None, 0, address15)

    def write(self, address15, in16):
        return self.memory.invoke(in16, 1, address15)
