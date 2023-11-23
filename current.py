from itertools import product


FILE_PATH = "perfaware/part1/listing_0040_challenge_movs"
FILE_PATH = "test"

with open(FILE_PATH, "rb") as file:
    bytes = file.read()
print(bytes)
bytes = b"\x00"
print(int.from_bytes(bytes[0:1], byteorder="little", signed=True))
