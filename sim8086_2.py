from argparse import ArgumentParser, FileType


# REG/RM-W field encoding (Table 4-9)
REGRM_W_ENC = {
    "0000": "al", "0010": "cl", "0100": "dl", "0110": "bl",
    "1000": "ah", "1010": "ch", "1100": "dh", "1110": "bh",
    "0001": "ax", "0011": "cx", "0101": "dx", "0111": "bx",
    "1001": "sp", "1011": "bp", "1101": "si", "1111": "di",
}


# Read command line argument: input file
parser = ArgumentParser()
parser.add_argument("file", type=FileType("rb"))
args = parser.parse_args()


# Processing file
print("bits 16", end="\n\n")
for bytes in args.file:
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
