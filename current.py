with open("test", "rb") as file:
    bytes_1 = file.read()
with open("perfaware/part1/listing_0041_add_sub_cmp_jnz", "rb") as file:
    bytes_2 = file.read() 
for n, (byte_1, byte_2) in enumerate(zip(bytes_1, bytes_2)):
    if byte_1 != byte_2:
        print(f"{n}: {bin(byte_1)[2:].zfill(8)}/{byte_1} - {bin(byte_2)[2:].zfill(8)}/{byte_2}")

"""
FILE_PATH = "perfaware/part1/listing_0041_add_sub_cmp_jnz"
FILE_PATH = "test"

with open(FILE_PATH, "rb") as file:
    bytes = file.read()
for byte in bytes:
    print(bin(byte)[2:].zfill(8))
"""


'''
from pprint import pprint


JMP = {
    "jz":     "01110100",
    "jnge":   "01111100",
    "jng":    "01111110",
    "jnae":   "01110010",
    "jna":    "01110110",
    "jpe":    "01111010",
    "jo":     "01110000",
    "js":     "01111000",
    "jnz":    "01110101",
    "jge":    "01111101",
    "jg":     "01111111",
    "jae":    "01110011",
    "ja":     "01110111",
    "jpo":    "01111011",
    "jno":    "01110001",
    "jns":    "01111001",
    "loope":  "11100001",
    "loopne": "11100000",
    "jcxz":   "11100011",
}


def from_bits(bins):
    return sum(2 ** n for n, bit in enumerate(reversed(bins)) if bit == "1")


jmps = {from_bits(bits): op for op, bits in JMP.items()}
with open("jumps.txt", "w") as file:
    pprint(jmps, sort_dicts=False, stream=file)
'''