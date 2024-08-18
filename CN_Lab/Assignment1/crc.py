

# Define CRC polynomials
CRC_POLYNOMIALS = {
    "CRC-8": "111010101",
    "CRC-10": "11011000101",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111"
}

def xor(a, b):
    """
    Perform XOR operation between two binary strings
    """
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)

def mod2div(dividend, divisor):
    
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword

def generate_crc_codeword(dataword, crc_type):
    polynomial = CRC_POLYNOMIALS[crc_type]
    l_key = len(polynomial)

    appended_data = dataword + '0' * (l_key - 1)
    remainder = mod2div(appended_data, polynomial)
    codeword = dataword + remainder
    return codeword

def validate_crc_codeword(codeword, crc_type):
    polynomial = CRC_POLYNOMIALS[crc_type]
    l_key = len(polynomial)

    remainder = mod2div(codeword, polynomial)
    return remainder.count('1') == 0