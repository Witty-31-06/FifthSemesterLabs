def generate_checksum(chunks):
    res = 0  # Initialize result as an integer for summing
    size = len(chunks[0])

    for chunk in chunks:
        res += int(chunk, 2)  # Add binary chunks as integers

    res_bin = bin(res)  # Convert result back to binary string
    res_bin = res_bin[2:]  # Remove '0b' prefix
    # Ensure res_bin is padded to at least 'size' bits
    res_bin = res_bin.zfill(size)

    # Handle carry bits
    while len(res_bin) > size:
        carry = res_bin[:-size]
        res_bin = res_bin[-size:]
        res_bin = bin(int(res_bin, 2) + int(carry, 2))[2:].zfill(size)

    # Return the checksum by flipping bits

    ans =  ''.join('1' if x == '0' else '0' for x in res_bin)
    print(ans)
    return ans

def check_checksum(chunks, checksum):
    res = 0  # Initialize result as an integer for summing
    size = len(chunks[0])

    for chunk in chunks:
        if chunk == '':
            continue
        res += int(chunk, 2)  # Add binary chunks as integers

    # Add the checksum
    res += int(checksum, 2)

    res_bin = bin(res)  # Convert result back to binary string
    res_bin = res_bin[2:]  # Remove '0b' prefix
    res_bin = res_bin.zfill(size)

    # Handle carry bits
    while len(res_bin) > size:
        carry = res_bin[:-size]
        res_bin = res_bin[-size:]
        res_bin = bin(int(res_bin, 2) + int(carry, 2))[2:].zfill(size)

    # Check if the result is all 1s
    return all(bit == '1' for bit in res_bin)

def generate_checksum_codeword(dataword):
    padded_dataword = dataword.ljust((len(dataword) + 15) // 16 * 16, '0')
    chunks = [padded_dataword[i:i+16] for i in range(0, len(padded_dataword), 16)]
    print('checksum chunks', chunks)
    checksum = generate_checksum(chunks)
    return dataword + checksum


def validate_checksum_codeword(codeword):
    # Split the codeword into 16-bit chunks, excluding the last 16 bits for checksum
    padded_codeword = codeword[:-16].ljust((len(codeword) - 16 + 15) // 16 * 16, '0')
    chunks = [padded_codeword[i:i+16] for i in range(0, len(padded_codeword), 16)]
    checksum = codeword[-16:]
    return check_checksum(chunks, checksum)
