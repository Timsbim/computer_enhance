from argparse import ArgumentParser, FileType
from itertools import product


# REG/RM-W field encoding (Table 4-9)
REGRM_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}

# R/M encoding for MOD = 00, 01, 10
RM_ENC = {
    0: "bx + si", 1: "bx + di", 2: "bp + si", 3: "bp + di",
    4: "si", 5: "di", 6: "bp", 7: "bx"
}


# Read command line argument: input file
parser = ArgumentParser()
parser.add_argument("file", type=FileType("rb"))
args = parser.parse_args()


print("; Listing produced by bit manipulation approach")
print("bits 16", end="\n\n")

# Read file
bytes = args.file.read()

# Processing data
num_bytes = len(bytes)
i = 0
while i < num_bytes:
    
    # Process first byte of instruction
    first_byte = bytes[i]
    i += 1
    if first_byte >> 2 == 34:  # Register/memory to/from register
        
        D  = (first_byte >> 1) & 1  # 7. bit
        W  = first_byte & 1         # 8. bit
        
        second_byte = bytes[i]
        i += 1
        MOD = second_byte >> 6        # First 2 bits
        REG = (second_byte >> 3) & 7  # Bits 3 - 5
        RM  = second_byte & 7         # Bits 6 - 8

        reg = REGRM_W_ENC[REG + W * 8]
        if MOD < 3:  # Memory mode
            
            disp = 0
            if MOD == 0:  # Memory mode, no displacement
                if RM == 6:  # Direct address
                    pass
            elif MOD == 1:  # 8-bit displacement
                disp = bytes[i]
                i += 1
            else:  # 16-bit displacement
                disp = int.from_bytes(bytes[i:i + 2], byteorder="little")
                i += 2
            mem = f"[{RM_ENC[RM]}" + (f" + {disp}]" if disp != 0 else "]")
            
            if D == 0:  # From register into memory
                print(f"mov {mem}, {reg}")
            else:  # From memory into register
                print(f"mov {reg}, {mem}")
        
        else:  # Register mode
            
            reg2 = REGRM_W_ENC[RM + W * 8]
            if D == 0:
                reg, reg2 = reg2, reg
            print(f"mov {reg}, {reg2}")
    
    elif first_byte >> 4 == 11:  # Immediate to register
        
        W   = (first_byte >> 3) & 1  # 5. bit
        if W == 0:
            DATA = bytes[i]
            i += 1
        else:
            DATA = int.from_bytes(bytes[i:i + 2], byteorder="little")
            i += 2
        print(f"mov {REGRM_W_ENC[(first_byte & 7) + W * 8]}, {DATA}")
    
    else:
        print("Instruction(s) unknown!")
