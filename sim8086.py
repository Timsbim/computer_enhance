from argparse import ArgumentParser, FileType
from itertools import product


# REG/RM-W field encoding (Table 4-9)
REGRM_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}


# Read command line argument: input file
parser = ArgumentParser()
parser.add_argument("file", type=FileType("rb"))
args = parser.parse_args()


# Processing file
print("bits 16", end="\n\n")
for bytes in args.file:
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
