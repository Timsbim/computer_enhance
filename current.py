from itertools import islice, product


FILE_PATH = "perfaware/part1/listing_0037_single_register_mov"
FILE_PATH = "perfaware/part1/listing_0038_many_register_mov"


# Approach with strings (binning)
W_REG_ENC = {
    bin(key).lstrip("0b").zfill(4): r + w
    for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {"1100": "sp", "1101": "bp", "1110": "si", "1111": "di"}
print(W_REG_ENC)

with open(FILE_PATH, "rb") as file:
    for bytes in file:
        bytes = [bin(byte).lstrip("0b") for byte in bytes.rstrip(b"\n")]
        
        # Evaluate the first 2 bytes
        first_byte = bytes[0]
        OPCODE = first_byte[:6]  # First 6 bits
        D      = first_byte[6]   # 7. bit
        W      = first_byte[7]   # 8. bit
        
        second_byte = bytes[1]
        MOD = second_byte[:2]   # First 2 bits
        REG = second_byte[2:5]  # Bits 3 - 5
        RM  = second_byte[5:]   # Bits 6 - 8

        if OPCODE == "100010" and MOD == "11":
            print(D, W, MOD, REG, RM)
        else:
            print("Instruction(s) unknown!")


# Approach with bit manipulation

# Register lookup
REG_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}

with open(FILE_PATH, "rb") as file:
    print("bits 16", end="\n\n")
    for bytes in file:
        
        # Evaluate the first 2 bytes
        first_byte = bytes[0]
        OPCODE = first_byte >> 2        # First 6 bits
        D      = (first_byte >> 1) & 1  # 7. bit
        W      = first_byte & 1         # 8. bit
        
        second_byte = bytes[1]
        MOD = second_byte >> 6        # First 2 bits
        REG = (second_byte >> 3) & 7  # Bits 3 - 5
        RM  = second_byte & 7         # Bits 6 - 8

        if OPCODE == 34 and MOD == 3:
            reg1 = REG_W_ENC[REG + W * 8]
            reg2 = REG_W_ENC[RM + W * 8]
            if D == 0:
                reg1, reg2 = reg2, reg1
            print(f"mov {reg1}, {reg2}")
        else:
            print("Instruction(s) unknown!")

