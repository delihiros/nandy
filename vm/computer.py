import cpu
import memory
import rom32k
import bus


class Computer:
    def __init__(self):
        self.rom = rom32k.ROM32K()
        self.memory = memory.Memory()
        self.bus = bus.Bus(self.rom, self.memory)
        self.cpu = cpu.CPU(bus)

    def load_rom(self, rom_file):
        self.rom.load(rom_file)

    def step(self):
        self.cpu.step()
