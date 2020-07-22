# Where to store variables if we have too many for the registers?

# Stack: push, pop, storage

# RAM == memory

# registers, caches, RAM, hard drive

# memory: a way to store info and get it back




# FF # 255
# FE 
# FD
# FC 
# FB
# FA 
# F9 
# F8
# F7
# F6
# F5
# F4 <-- SP (stack pointer) 
# F3
# ...
# 04: 00
# 03: 83
# 02: PRINT_NUM
# 01: PRINT_TIM
# 00: PRINT_TIM

PRINT_TIM    =  0b00000001
HALT         =  0b10  # 2
PRINT_NUM    =  0b00000011  # opcode 3
SAVE         =  0b100
PRINT_REG    =  0b101    # opcode 5
ADD          =  0b110
PUSH         =  0b111 
POP          =  0b1000 # opcode 8

# registers[2] = registers[2] + registers[3]

# First up, here's our messy file where we worked through bitwise logical operations, bit shifting left and right, and bit masking. You can now make bits do what you what! :thematrixcode:
# bitwise.txt 
# AND, OR, NOT, XOR
# Operation    Boolean Operator     Bitwise Operator
# AND             &&  (and)              &
# OR               ||  (or)              |
# NOT              !  (not)              ~
# XOR                none!               ^
# OR: "At least one or the other"
# AND       True && True --> True
#           True && False --> False
#           False && False --> False
# OR        True || False --> True
#            1    |   0   --> 1
#           True || True  --> True
#             1   |   1   -->   1
#           False || False --> False
#             0    |   0   -->  0
# NOT         !(True) --> False
#               ~1    --> 0
#              !(False) --> True
#              ~0      --> 1
# XOR           True xor False --> True
#               True xor True  --> False
#               False xor False --> False
#   0b1010101
# ^ 0b1000101
# -----------
#   0b0010000
#   0b0011100
# ^ 0b1010101
# -----------
#   0b1001001
#   ~0b001110
#    0b110001
# if (True and True):
# if (True and False)
# if a or b:
# if (True && False) {}
# if (a || b) {}
#   0b1010101
# & 0b1000101
# -----------
#   0b1001101
#   0b0011100
# & 0b1010101
# -----------
#   0b0010100
#   0b1010101
# | 0b1000101
# -----------
#   0b1010101
#   0b0011100
# | 0b1010101
# -----------
#   0b1011101
# Shifting
# Right Shifting
# 0b10101010
#  0b101010 >> 1
#   0b10101 >> 2
#    0b1010 >> 3
# 00010101
# Left Shifting
#   10101010 << 1
# 101010100  << 2
# How to isolate bits that we are interested in?
# Left shift!
#  10101010 >> 6
#  10
#     vv
#  10101010 
#  10101010 >> 3
#     vv
#  10101 
#  10101  << 3
#  10101000
# Masking!
#   1010
# & 0011
# ------
#   0010
#       vv
#    10101 
# &  00011 
# --------
#    00001
#   01010101
# & 11111111
# ----------
#   01010101
#   01010101
# & 00000000 
# ----------
#   00000000       
# AABBCCDD
# ADD  register1 register
#   10100000 >> 6
#           10
# pc += 1 + (command >> 6)
#       01 + 10 == 11
# if command == ADD:
#     pc += 2
# HALT
#   00000001
# memory = [
#     ADD,
#     register1,
#     register2,
#     HALT,
# ]
# try:
#     file = open("print8.ls8", 'r')
#     lines = file.read()
#     # print(lines)
#     raise Exception('hi')
# except Exception:
#     print(file.closed)
# try:
#     filename = sys.argv[1]
# except IndexError:
#     print('Error Message')
#     sys.exit()

# import sys

# if len(sys.argv) < 2:
#     print("Please pass in a second filename: python3 in_and_out.py second_filename.py")
#     sys.exit()
# ​
# file_name = sys.argv[1]
# try:
#     with open(file_name) as file:
#         for line in file:
#             split_line = line.split('#')[0]
#             # remove whitespace
#             command = split_line.strip()
# ​               
#             # skip blank lines
#             if command == '':
#                 continue
# ​           
#             # convert string to int (2 = base 2)
#             num = int(command, 2)
# ​
#             print(f'{num:8b} is {num}')
            
# ​
# except FileNotFoundError:
#     print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
#     sys.exit()

import sys

memory = [0] * 256

def load_memory(file_name):
    try:
        address = 0
        with open(file_name) as file:
            for line in file:
                split_line = line.split("#")[0]
                command = split_line.strip()

                if command == "":
                    continue

                instruction = int(command, 2)
                memory[address] = instruction

                address += 1
    
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {sys.argv[1]} file was not found")
        sys.exit()

if len(sys.argv) < 2:
    print("Please pass in a second filename: python3 in_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1]
load_memory(file_name)

# write a program to pull each command out of memory and execute
# We can loop over it!

# register aka memory
registers = [0] * 8
# [0,0,99,0,0,0,0,0]
# R0-R7
# R7 reserved for SP
registers[7] = 0xF4

pc = 0
running = True
while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim!")

    if command == HALT:
        running = False
    
    if command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 1

    if command == SAVE:
        reg = memory[pc + 1]
        num_to_save = memory[pc + 2]
        registers[reg] = num_to_save

        pc += 2

    if command == PRINT_REG:
        reg_index = memory[pc + 1]
        print(registers[reg_index])
        pc += 1

    if command == ADD:
        first_reg = memory[pc + 1]
        sec_reg = memory[pc + 2]
        registers[first_reg] = registers[first_reg] + registers[sec_reg]
        pc += 2

    if command == PUSH:
        # decrement stack pointer
        registers[7] -= 1

        # get a value from the given register
        reg = memory[pc + 1]
        value = registers[reg]

        # put at stack pointer address
        sp = registers[7]
        memory[sp] = value
        pc += 1
        
    if command == POP:
        # get the stack pointer (where do we look?)
        sp = registers[7]
        # get register number to put value in
        reg = memory[pc + 1]
        # use stack pointer to get the value
        value = memory[sp]
        # put the value into the given register
        registers[reg] = value
        # increment our stack pointer
        registers[7] += 1
        # increment our program counter
        pc += 1

    pc += 1