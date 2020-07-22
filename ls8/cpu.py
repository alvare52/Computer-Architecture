"""CPU functionality."""

import sys

# instructions

HLT = 0b00000001 # stop running
PRN = 0b01000111 # prints value at register given
LDI = 0b10000010 # sets a specified register to a specified value
MUL = 0b10100010 # multiplies. reg1 *= reg2 (MUL, reg1, reg2)
ADD = 0b10100000 # adds. reg1 += reg2 (ADD, reg1, reg2)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # registers 0-7
        self.pc = 0 # counter
        self.ram = [0] * 256 # 256 bytes of memory?
        self.running = True

    def load(self, file_name):
        """Load a program into memory."""
        # Day 2 - 
        # give file_name parameter (basically simple01.py but run with mult.ls8)
        # read commands in that file instead of hardcoded ones here
        # also add a mult command thing

        # OLD
        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split("#")[0]
                    command = split_line.strip()

                    if command == "":
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction

                    address += 1
    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file was not found")
            sys.exit()
        
        # OLD
        # for instruction in file:
        #     self.ram[address] = instruction
        #     address += 1

    # arithasdfma'sdf
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        # first 2 bits say how many operands there are 
        # self.pc += 1 + (op >> 6) # ?
        print(f"ALU - {op}")
        if op == "ADD":
            print("inside ADD block")
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        #elif op == "SUB": etc

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        print(" - RUN - ")
        

        while self.running:
            
            command = self.ram[self.pc]

            if command == HLT:
                print(" - HLT - ")
                self.running = False 

            if command == LDI:
                print("LDI")

                # thing thats right after LDI (ex: R0)
                reg_index = self.ram[self.pc + 1]
                # second thing after LDI (ex: 8)
                num_to_save = self.ram[self.pc + 2]
                self.reg[reg_index] = num_to_save
                # self.pc += 2 # delete this later

            if command == PRN:
                print("PRN")
                # print out whatever's in the register after PRN
                reg_index = self.ram[self.pc + 1]
                print(f"R{reg_index} is {self.reg[reg_index]}")
                # self.pc += 1

            if command == MUL:
                print("MUL")
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("MUL", a, b)

            if command == ADD:
                print("ADD")
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("ADD", a, b)

            # change so this looks at command >> 6 (this chops off last 6 bits)
            self.pc += 1 + (command >> 6)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

if len(sys.argv) < 2:
    print("Please pass in a second filename: python3 in_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1]
# load_memory(file_name)

cpu = CPU()

cpu.load(file_name)
cpu.run()