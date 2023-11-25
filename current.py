from itertools import product


FILE_PATH = "perfaware/part1/listing_0041_add_sub_cmp_jnz"
FILE_PATH = "test"

with open(FILE_PATH, "rb") as file:
    bytes = file.read()
for byte in bytes:
    print(bin(byte)[2:].zfill(8))
