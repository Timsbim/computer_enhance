from itertools import product


FILE_PATH = "perfaware/part1/listing_0037_single_register_mov"
FILE_PATH = "perfaware/part1/listing_0038_many_register_mov"


# Approach with strings (binning)

# REG/RM-W field encoding (Table 4-9)
REGRM_W_ENC = {
    "0000": "al", "0010": "cl", "0100": "dl", "0110": "bl",
    "1000": "ah", "1010": "ch", "1100": "dh", "1110": "bh",
    "0001": "ax", "0011": "cx", "0101": "dx", "0111": "bx",
    "1001": "sp", "1011": "bp", "1101": "si", "1111": "di",
}


print("; Listing produced by string manipulation approach")
print("bits 16", end="\n\n")

# Processing file
with open(FILE_PATH, "rb") as file:
    for bytes in file:
        # Converting line of bytes into bin-strings (after removing eol chars)
        bytes = [bin(byte).lstrip("0b") for byte in bytes.rstrip()]    

        # Split byte stream into consecutive pairs
        for i in range(0, len(bytes), 2):
            
            first_byte = bytes[i]
            OP = first_byte[:6]  # First 6 bits
            D  = first_byte[6]   # 7. bit
            W  = first_byte[7]   # 8. bit
            
            second_byte = bytes[i + 1]
            MOD = second_byte[:2]   # First 2 bits
            REG = second_byte[2:5]  # Bits 3 - 5
            RM  = second_byte[5:]   # Bits 6 - 8
    
            if OP == "100010" and MOD == "11":
                reg1 = REGRM_W_ENC[REG + W]
                reg2 = REGRM_W_ENC[RM + W]
                if D == "0":
                    reg1, reg2 = reg2, reg1
                print(f"mov {reg1}, {reg2}")
            else:
                print("Instruction(s) unknown!")


# Approach with bit manipulation
print("\n")

# REG/RM-W field encoding (Table 4-9)
REGRM_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}


print("; Listing produced by bit manipulation approach")
print("bits 16", end="\n\n")

# Processing file
with open(FILE_PATH, "rb") as file:
    for bytes in file:
        # Remove eol chars
        bytes = bytes.rstrip()
        
        # Split byte stream into consecutive pairs
        for i in range(0, len(bytes), 2):
            
            first_byte = bytes[i]
            OP = first_byte >> 2        # First 6 bits
            D  = (first_byte >> 1) & 1  # 7. bit
            W  = first_byte & 1         # 8. bit
            
            second_byte = bytes[i + 1]
            MOD = second_byte >> 6        # First 2 bits
            REG = (second_byte >> 3) & 7  # Bits 3 - 5
            RM  = second_byte & 7         # Bits 6 - 8
    
            if OP == 34 and MOD == 3:
                reg1 = REGRM_W_ENC[REG + W * 8]
                reg2 = REGRM_W_ENC[RM + W * 8]
                if D == 0:
                    reg1, reg2 = reg2, reg1
                print(f"mov {reg1}, {reg2}")
            else:
                print("Instruction(s) unknown!")
