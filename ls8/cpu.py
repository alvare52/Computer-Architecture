"""CPU functionality."""

import sys

# instructions

HLT = 0b00000001 # stop running
PRN = 0b01000111 # prints value at register given
LDI = 0b10000010 # sets a specified register to a specified value

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # registers 0-7
        self.pc = 0 # counter
        self.ram = [0] * 256 # 256 bytes of memory?
        self.running = True

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # arithasdfma'sdf
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        # first 2 bits say how many operands there are 
        # self.pc += 1 + (op >> 6) # ?

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
                print(f"Register: {reg_index}, value: {self.reg[reg_index]}")
                # self.pc += 1

            # change so this looks at command >> 6 (this chops off last 6 bits)
            self.pc += 1 + (command >> 6)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
