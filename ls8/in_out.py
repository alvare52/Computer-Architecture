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

import sys

if len(sys.argv) < 2:
    print("Please pass in a second filename: python3 in_out.py second_filename.py")
    sys.exit()

file_name = sys.argv[1] # second argument passed in
try:
    with open(file_name) as file:
        for line in file:
            split_line = line.split("#")[0]
            command = split_line.strip()

            if command = "":
                continue 

            num = int(command, 2)

            print(f"{num:8b} is {num}")

except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} file was not found")
    sys.exit()


# # BITWISE OPERTIONS, SHIFTING, AND MASKING
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