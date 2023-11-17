"""
The first byte — eight bits — has the pattern 100010 in its high six bits.
That is what indicates that it will be a mov instruction specifically.
The bottom two bits actually encode options for the move instruction. Bit 1 is
the D bit, and bit 0 is the W bit, and they can both be set to either 0 or 1
to encode different options for are move (which we’ll see shortly).

You can already see the complexity start to creep in a little bit here! Intel
instruction encodings have a bit of a reputation for unnecessary complexity,
and you’re getting a taste of that already.

Anyway, the second byte in the two-byte sequence encodes three separate
things. The high two bits are the mod field, then the low six bits are split
three and three for the reg field and the r/m field.

These are all the bits involved in a register-to-register move instruction.
Let’s look at what they all mean.

The two-bit mod field is a code that tells us what kind of move this is: is it
between two registers, or between a register and memory? Since we’re only
looking at register-register moves, the value will always be 11 (since we’re
talking about bits, that’s two 1 bits, not eleven!). 11 is the code for
“register to register”.

The three-bit reg and r/m fields encode the two registers involved in the
move. Three bits for each gives 8 possible names for each register. How does
this correspond to ax, bx, etc.? Well, there’s actually a special table that
defines the mapping, which we’ll see when we look at this on the computer.

But how do we know which of the two encoded registers is the source and which
is the destination? That’s where the d bit comes in — it’s the destination
bit. If the d bit is 1, then the reg register is the destination. If the d bit
is 0, then the reg register is the source. And by process of elimination,
whichever one the reg register is not, the r/m register is.

Finally, we have the w bit, which says whether the instruction is going to be
wide, meaning that it will operate on 16 bits. When the w bit is 0, it means
the mov will copy 8 bits. If the w bit is 1, it means the mov will copy 16
bits.

In addition to saying how many bits to copy, the w bit also therefore
implicitly says how much of a register is being targeted by the copy. If it is
only copying 8 bits, then by definition it would only be reading from half of
the source register. What would this look like in the assembly language?

Well, in addition to naming the entire 16-bit register with ax, bx, and so on,
you can also refer just to the high 8 or low 8 bits of a register using “l”
and “h”. So “x” is, in some sense, less part of the register name and more of
a notation for “all 16 bits”. The register name is perhaps more properly just
“a”, and then the suffix x, l, or h is appended to say how much of the
register you are talking about. So this:
```
mov al, bl
```
would copy just the low 8 bits, unlike the ax/bx version which copied all 16.
"""


FILE_PATH = "perfaware/part1/listing_0037_single_register_mov"
#FILE_PATH = "perfaware/part1/listing_0038_many_register_mov"


# Approach with strings (binning)
with open(FILE_PATH, "rb") as file:
    for bytes in file:
        bytes = [bin(byte).lstrip("0b") for byte in bytes.rstrip(b"\n")]
        
        # Evaluate the first 2 bytes
        first_byte, second_byte = bytes[0], bytes[1]
        OPCODE, D, W = first_byte[:6], first_byte[6], first_byte[7]
        MOD, REG, R_M = second_byte[:2], second_byte[2:5], second_byte[5:]
        
        if OPCODE == "100010":  # MOV
            print(D, W, MOD, REG, R_M)
        else:
            print("Instruction unknown!")


# Approach with bit manipulation
from itertools import product

REG_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}
print(REG_W_ENC)

REG_W_ENC = {
    bin(key).lstrip("0b").zfill(4): r + w
    for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {"1001": "sp", "1011": "bp", "1101": "si", "1111": "di"}
print(REG_W_ENC)

REG_W_ENC = {
    0: "al", 1: "cl", 2: "dl", 3: "bl", 4: "ah", 5: "ch", 6: "dh", 7: "bh",
    8: "ax", 9: "cx", 10: "dx", 11: "bx", 12: "sp", 13: "bp", 14: "si", 15: "di"
}

with open(FILE_PATH, "rb") as file:
    for bytes in file:
        # Evaluate the first 2 bytes
        first_byte, second_byte = bytes[0], bytes[1]
        OPCODE, D, W = first_byte >> 2, (first_byte >> 1) & 1, first_byte & 1
        MOD, REG, R_M = second_byte >> 6, (second_byte >> 3) & 7, second_byte & 7
        
        if OPCODE == 34:  # MOV
            print(D, W, MOD, REG, R_M)
        else:
            print("Instruction unknown!")


# REG + W * 8