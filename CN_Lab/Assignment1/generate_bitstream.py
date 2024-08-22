#!/usr/bin/env python3
import random
import sys
def generate_bitstream(length):
    return ''.join(random.choice('01') for _ in range(length))

def write_bitstream_to_file(bitstream, filename):
    with open(filename, 'w') as file:
        file.write(bitstream)

if len(sys.argv) != 3:
    print("Usage: python generate_bitstream.py <length> <filename>")
    exit(1)

filename = sys.argv[2]
length = int(eval(sys.argv[1]))
# print(filename, length)
bitstream = generate_bitstream(length)
write_bitstream_to_file(bitstream, filename)
# print("File created... ", filename)
print(f"{length} bits written to {filename}")