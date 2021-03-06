import bit

class CPU:
    def __init__(self, bus):
        self.bus = bus
        self.pc = 0
        self.addressing_register = 0
        self.data_register = 0


    def fetch(self):
        return self.bus.read_rom(self.pc)

    def decode(self, op):
        op_type = bit.nth(op, 15)
        if op_type == 0: # Op A
            data = bit.extract(op, 0, 15)
            return {'op_type': op_type, 'data': data, 'readable': ['C', bin(data)]}
        else: # Op C
            comp = bit.extract(op, 6, 13) # a, cccccc
            dest = bit.extract(op, 3, 5) # ddd
            jump = bit.extract(op, 0, 2) # jjj
            print({'op': bin(op), 'comp': bin(comp), 'dest': bin(dest), 'jump': bin(jump)})

            return {'op_type': op_type, 'comp': comp, 'dest': dest, 'jump': jump, 'readable': ['A']}

    def compute(self, comp):
        if comp == 0b0101010:
            return 0
        elif comp == 0b0111111:
            return 1
        elif comp == 0b0111010:
            return -1
        elif comp == 0b0001100:
            return self.data_register
        elif comp == 0b0110000:
            return self.addressing_register
        elif comp == 0b0001101:
            return self.data_register
        elif comp == 0b0110001:
            return ~self.addressing_register
        elif comp == 0b0001111:
            return -self.data_register
        elif comp == 0b0110011:
            return -self.addressing_register
        elif comp == 0b0011111:
            return self.data_register + 1
        elif comp == 0b0110111:
            return self.addressing_register + 1
        elif comp == 0b0001110:
            return self.data_register - 1
        elif comp == 0b0110010:
            return self.addressing_register - 1
        elif comp == 0b0000010:
            return self.data_register + self.addressing_register
        elif comp == 0b0010011:
            return self.data_register - self.addressing_register
        elif comp == 0b0000111:
            return self.addressing_register - self.data_register
        elif comp == 0b0000000:
            return self.data_register & self.addressing_register
        elif comp == 0b0010101:
            return self.data_register | self.addressing_register
        elif comp == 0b1110000:
            return self.bus.read(self.addressing_register)
        elif comp == 0b1110001:
            return ~self.bus.read(self.addressing_register)
        elif comp == 0b1110011:
            return -self.bus.read(self.addressing_register)
        elif comp == 0b1110111:
            return self.bus.read(self.addressing_register) + 1
        elif comp == 0b1110010:
            return self.bus.read(self.addressing_register) - 1
        elif comp == 0b1000010:
            return self.data_register + self.bus.read(self.addressing_register)
        elif comp == 0b1010011:
            return self.data_register - self.bus.read(self.addressing_register)
        elif comp == 0b1000111:
            return self.bus.read(self.addressing_register) - self.data_register
        elif comp == 0b1000000:
            return self.data_register & self.bus.read(self.addressing_register)
        elif comp == 0b1010101:
            return self.data_register | self.bus.read(self.addressing_register)

    def jmp(self, jump, result):
        if jump == 0b000:
            self.pc += 1
        elif jump == 0b001 and result > 0:
            self.pc = self.addressing_register
        elif jump == 0b010 and result == 0:
            self.pc = self.addressing_register
        elif jump == 0b011 and result >= 0:
            self.pc = self.addressing_register
        elif jump == 0b100 and result < 0:
            self.pc = self.addressing_register
        elif jump == 0b101 and result != 0:
            self.pc = self.addressing_register
        elif jump == 0b110 and result <= 0:
            self.pc = self.addressing_register
        elif jump == 0b111:
            self.pc = self.addressing_register
        else:
            self.pc += 1

    def execute(self, decoded):
        if decoded['op_type'] == 0:
            self.addressing_register = decoded['data']
            self.pc += 1
        elif decoded['op_type'] == 1:
            result = self.compute(decoded['comp'])
            if bit.nth(decoded['dest'], 0) == 1:
                self.bus.write(self.addressing_register, result)
            if bit.nth(decoded['dest'], 1) == 1:
                self.data_register = result
            if bit.nth(decoded['dest'], 2) == 1:
                self.addressing_register = result
            self.jmp(decoded['jump'], result)

    def step(self):
        self.op = self.fetch()
        self.decoded = self.decode(self.op)
        self.result = self.execute(self.decoded)
        # print(self.pc, '0b{:016b}'.format(op, 2), decoded, self.data_register, self.addressing_register)
