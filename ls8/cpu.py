"""CPU functionality."""

import sys

# instructions

HLT = 0b00000001 # stop running
PRN = 0b01000111 # prints value at register given
LDI = 0b10000010 # sets a specified register to a specified value
MUL = 0b10100010 # multiplies. reg1 *= reg2 (MUL, reg1, reg2)
ADD = 0b10100000 # adds. reg1 += reg2 (ADD, reg1, reg2)
POP = 0b01000110 # Pop the value at the top of the stack into the given register
PUSH = 0b01000101 # Push the value in the given register on the stack.
CALL = 0b01010000 # Calls a subroutine (function) stored at address in the following register
RET = 0b00010001 # Return from subroutine. Pop the value from the top of the stack and store it in the PC

# Sprint stuff
CMP = 0b10100111 # Compare 2 registers and sets flag property accordingly
JMP = 0b01010100 # Jump to the address stored in the given register and set pc to address stored in given register 
JEQ = 0b01010101 # if equal flag is 1, jump to address stored in the given register
JNE = 0b01010110 # if equal flag is 0, jump to address stored in the given register

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # registers 0-7
        self.pc = 0 # counter
        self.ram = [0] * 256 # 256 bytes of memory?
        self.running = True
        # NEW
        self.reg[7] = 0xF4
        # NEW for Sprint
        self.fl = 0b00000000 # 00000LGE

    #         The flags register `FL` holds the current flags status. These flags
    # can change based on the operands given to the `CMP` opcode.

    # The register is made up of 8 bits. If a particular bit is set, that flag is "true".

    # `FL` bits: `00000LGE`

    # * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
    # zero otherwise.
    # * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
    # registerB, zero otherwise.
    # * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
    # otherwise.

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
                    # 
                    split_line = line.split("#")[0]
                    # remove white spaces
                    command = split_line.strip()

                    # skip empty lines
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
            # print("inside ADD block")
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b00000001 # 00000LGE
            elif reg_a < reg_b:
                self.fl = 0b00000100
            elif reg_a > reg_b:
                self.fl = 0b00000010

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
                self.pc += 1 + (command >> 6)

            if command == PRN:
                print("PRN")
                # print out whatever's in the register after PRN
                reg_index = self.ram[self.pc + 1]
                print(f"R{reg_index} is {self.reg[reg_index]}")
                # self.pc += 1
                self.pc += 1 + (command >> 6)

            if command == MUL:
                print("MUL")
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("MUL", a, b)
                self.pc += 1 + (command >> 6)

            if command == ADD:
                print("ADD")
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("ADD", a, b)
                self.pc += 1 + (command >> 6)

            if command == PUSH:
                # decrement stack pointer
                self.reg[7] -= 1

                # get a value from the given register
                reg = self.ram[self.pc + 1]
                value = self.reg[reg]

                # put at stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value
                # pc += 1
                self.pc += 1 + (command >> 6)
        
            if command == POP:
                # get the stack pointer (where do we look?)
                sp = self.reg[7]
                # get register number to put value in
                reg = self.ram[self.pc + 1]
                # use stack pointer to get the value
                value = self.ram[sp]
                # put the value into the given register
                self.reg[reg] = value
                # increment our stack pointer
                self.reg[7] += 1
                # increment our program counter
                # pc += 1
                self.pc += 1 + (command >> 6)

            if command == CALL:
                # get register number
                reg = self.ram[self.pc + 1]
                # get the address to jump to, from the register
                address = self.reg[reg]
                # push command after CALL onto the stack
                return_address = self.pc + 2
                # decrement stack pointer
                self.reg[7] -= 1
                sp = self.reg[7]
                # put return address on the stack
                self.ram[sp] = return_address
                # then look at register, jump to that address
                self.pc = address

            if command == RET:
                # pop the return address off the stack
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                # go to return address: set the pc to return address
                self.pc = return_address

            # change so this looks at command >> 6 (this chops off last 6 bits)

            if command == CMP:
                print("CMP")
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.alu("CMP", a, b)
                self.pc += 1 + (command >> 6) #?

            if command == JMP:
                self.pc += 1 + (command >> 6)

            if command == JEQ:
                self.pc += 1 + (command >> 6)

            if command == JNE:
                self.pc += 1 (command >> 6)
            

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value



# MAIN

if len(sys.argv) < 2:
    print("Please pass in a second filename: python3 in_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1]
# load_memory(file_name)

cpu = CPU()

cpu.load(file_name)
cpu.run()