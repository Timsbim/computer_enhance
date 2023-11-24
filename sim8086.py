from argparse import ArgumentParser, FileType
from itertools import product


# REG/RM-W field encoding (table 4-9)
REGRM_W_ENC = {
    key: r + w for key, (w, r) in enumerate(product("lhx", "acdb"))
} | {12: "sp", 13: "bp", 14: "si", 15: "di"}

# R/M encoding for MOD = 00, 01, 10 (table 4-10)
RM_ENC = {
    0: "bx + si", 1: "bx + di", 2: "bp + si", 3: "bp + di",
    4: "si", 5: "di", 6: "bp", 7: "bx"
}


def from_bytes(bytes, i, width, signed=False):
    offset = i + width
    bytes = bytes[i: offset]
    return offset, int.from_bytes(bytes, byteorder="little", signed=signed)


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
    
    if 80 <= (first_byte >> 1) <= 81:  # From/to memory to/from accumulator
        
        D  = (first_byte >> 1) & 1  # 7. bit
        W  = first_byte & 1         # 8. bit

        i, addr = from_bytes(bytes, i, W + 1)
        
        if D == 0:  # Memory-to-accumulator
            print(f"mov ax, [{addr}]")
        else:  # Accumulator-to-memory
            print(f"mov [{addr}], ax")
        
    elif first_byte >> 1 == 99:  # Intermediate to register/memory
        
        W  = first_byte & 1  # 8. bit
    
        second_byte = bytes[i]
        i += 1
        MOD = second_byte >> 6  # First 2 bits
        RM  = second_byte & 7   # Bits 6 - 8

        if MOD < 3:  # Memory mode
            
            if MOD == 0 and RM == 6:  # Direct address
                i, disp = from_bytes(bytes, i, 2, True)
                regmem = f"[{disp}]"
            else:
                if MOD == 0:
                    disp = 0
                else:
                    i, disp = from_bytes(bytes, i, MOD, True)

                regmem = f"[{RM_ENC[RM]}" + (f" + {disp}]" if disp != 0 else "]")
        
        else:  # Register mode
            regmem = REGRM_W_ENC[RM + W * 8]
        
        i, data = from_bytes(bytes, i, W + 1)
        data = ("byte" if W == 0 else "word") + str(data)
        print(f"mov {regmem}, {data}")
    
    elif first_byte >> 2 == 34:  # Register/memory to/from register
        
        D  = (first_byte >> 1) & 1  # 7. bit
        W  = first_byte & 1         # 8. bit
        
        second_byte = bytes[i]
        i += 1
        MOD = second_byte >> 6        # First 2 bits
        REG = (second_byte >> 3) & 7  # Bits 3 - 5
        RM  = second_byte & 7         # Bits 6 - 8

        reg = REGRM_W_ENC[REG + W * 8]
        if MOD < 3:  # Memory mode            
            if MOD == 0 and RM == 6:  # Direct address
                disp = int.from_bytes(bytes[i:i + 2], byteorder="little", signed=True)
                i += 2
                mem = f"[{disp}]"
            else:
                if MOD == 0:
                    disp = 0
                else:
                    i, disp = from_bytes(bytes, i, MOD, True)
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

        i, data = from_bytes(bytes, i, W + 1)
        
        print(f"mov {REGRM_W_ENC[(first_byte & 7) + W * 8]}, {data}")
    
    else:
        print("Instruction(s) unknown!")
