import sys
import time
import cpu
import memory
import rom32k
import bus


class Computer:
    def __init__(self):
        self.rom = rom32k.ROM32K()
        self.memory = memory.Memory()
        self.bus = bus.Bus(self.rom, self.memory)
        self.cpu = cpu.CPU(self.bus)

    def load_rom(self, rom_file):
        self.rom.load(rom_file)

    def step(self):
        self.cpu.step()
        print(self.cpu.pc, self.memory._memory[:16], 'D', self.cpu.data_register, 'A', self.cpu.addressing_register)

def __main__():
    computer = Computer()
    computer.load_rom(sys.argv[1])
    while True:
        computer.step()
        time.sleep(1)


if __name__ == '__main__':
    __main__()
