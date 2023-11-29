# Disassembling 8086 binaries

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

# Jumps
JMP_ENC = {
    116: "jz", 124: "jnge", 126: "jng", 114: "jnae", 118: "jna", 122: "jpe",
    112: "jo", 120: "js", 117: "jnz", 125: "jge", 127: "jg", 115: "jae",
    119: "ja", 123: "jpo", 113: "jno", 121: "jns", 226: "loop", 225: "loope",
    224: "loopne", 227: "jcxz"
}


parser = ArgumentParser()
parser.add_argument("file", type=FileType("rb"))
args = parser.parse_args()


print("bits 16", end="\n\n")

bytes = args.file.read()
i = 0


def from_bytes(width):
    global i
    n = int.from_bytes(bytes[i:i + width], byteorder="little", signed=True)
    i += width
    return n


while i < len(bytes):
    
    first_byte = bytes[i]
    i += 1

    # MOV: from/to memory to/from accumulator
    if 80 <= (first_byte >> 1) <= 81:
        
        D = (first_byte >> 1) & 1
        W = first_byte & 1

        addr = from_bytes(W + 1)
        
        if D == 0:  # Memory-to-accumulator
            print(f"mov ax, [{addr}]")
        else:  # Accumulator-to-memory
            print(f"mov [{addr}], ax")

    # MOV, ADD, SUB, CMP: intermediate to/from/with register/memory
    elif (OP := (first_byte >> 1)) == 99 or (first_byte >> 2) == 32:

        W  = first_byte & 1
    
        second_byte = bytes[i]
        i += 1
        MOD = second_byte >> 6
        RM  = second_byte & 7

        if OP == 99:
            op = "mov"
        else:
            op = {0: "add", 5: "sub", 7: "cmp"}.get((second_byte >> 3) & 7)
    
        if MOD < 3:  # Memory mode
    
            if MOD == 0 and RM == 6:  # Direct address
                regmem = f"[{from_bytes(2)}]"
            else:
                disp = from_bytes(MOD)
                regmem = f"[{RM_ENC[RM]}" + (f" + {disp}]" if disp != 0 else "]")
            if op != "mov":
                regmem = ("byte" if W == 0 else "word") + f" {regmem}"
        
        else:  # Register mode
            regmem = REGRM_W_ENC[RM + W * 8]

        if op == "mov":
            data = ("byte" if W == 0 else "word") + f" {from_bytes(W + 1)}"
        else:
            S  = (first_byte >> 1) & 1
            data = from_bytes(2 if S == 0 and W == 1 else 1)
    
        print(f"{op} {regmem}, {data}")

    # MOV, ADD, SUB, CMP: register/memory to/from register
    elif (OP := (first_byte >> 2)) in {0, 10, 14, 34}:

        op = {0: "add", 10: "sub", 14: "cmp"}.get(OP, "mov")
        
        D = (first_byte >> 1) & 1
        W = first_byte & 1
        
        second_byte = bytes[i]
        i += 1
        MOD = second_byte >> 6
        REG = (second_byte >> 3) & 7
        RM  = second_byte & 7

        reg = REGRM_W_ENC[REG + W * 8]
        if MOD < 3:  # Memory mode
            
            if MOD == 0 and RM == 6:  # Direct address
                regmem = f"[{from_bytes(2)}]"
            else:
                disp = from_bytes(MOD)
                regmem = f"[{RM_ENC[RM]}" + (f" + {disp}]" if disp != 0 else "]")
            
        else:  # Register mode
            regmem = REGRM_W_ENC[RM + W * 8]

        if D == 0:  # From register into register/memory
            print(f"{op} {regmem}, {reg}")
        else:  # From register/memory into register
            print(f"{op} {reg}, {regmem}")

    # MOV: immediate to register
    elif first_byte >> 4 == 11:
        
        W  = (first_byte >> 3) & 1
        data = from_bytes(W + 1)
        print(f"mov {REGRM_W_ENC[(first_byte & 7) + W * 8]}, {data}")
    
    # ADD, SUB, CMP: Immediate to/from/with accumulator
    elif (OP := (first_byte >> 1)) in {2, 22, 30}:

        W = first_byte & 1
        op = {2: "add", 22: "sub", 30: "cmp"}.get(OP)
        acc = "ax" if W == 1 else "al"
        print(f"{op} {acc}, {from_bytes(W + 1)}")

    # Jumps
    elif first_byte in JMP_ENC:
        print(f"{JMP_ENC[first_byte]} ${from_bytes(1) + 2:+}")     
    else:
        print(f"Instruction(s) unknown: {bin(first_byte)[2:].zfill(8)}")
