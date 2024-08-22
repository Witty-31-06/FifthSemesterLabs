import random


def generate_unique_auto_integers(x, n):
    if x > n + 1:
        raise ValueError("x must be less than or equal to n+1")
    return random.sample(range(n + 1), x)


def inject_multi_bit_error(codeword, indices):
    if any(index < 0 or index >= len(codeword) for index in indices):
        raise ValueError("Indices out of range")
    infected_codeword = list(codeword)
    for index in indices:
        infected_codeword[index] = '0' if codeword[index] == '1' else '1'
    return ''.join(infected_codeword)

def inject_odd_number_of_errors(codeword, indices):
    if any(index < 0 or index >= len(codeword) for index in indices):
        raise ValueError("Indices out of range")
    infected_codeword = list(codeword)
    for index in indices:
        infected_codeword[index] = '0' if codeword[index] == '1' else '1'
    return ''.join(infected_codeword)

def burst_error(codeword, start_index, burst_length):
    if start_index < 0 or start_index + burst_length > len(codeword):
        raise ValueError("Burst error out of range")
    infected_codeword = list(codeword)
    for i in range(start_index, start_index + burst_length):
        infected_codeword[i] = '0' if codeword[i] == '1' else '1'
    return ''.join(infected_codeword)

def inject_error_auto(codeword, error_type, burst_length=None):

    indices = generate_unique_auto_integers(3, len(codeword) - 1)
    if error_type == "MULTI_BIT":
        return inject_multi_bit_error(codeword, indices), indices
    elif error_type == "BURST":
        if burst_length is None:
            raise ValueError("Burst length must be provided for burst errors.")
        start_index = random.randint(0, len(codeword) - burst_length)
        return burst_error(codeword, start_index, burst_length)
    else:
        raise ValueError("Invalid error type specified.")


def inject_error_manual(codeword, error_type, indices=None, start_index=None, burst_length=None):
    if error_type == "MULTI_BIT":
        return inject_multi_bit_error(codeword, indices)
    elif error_type == "BURST":
        if start_index is None or burst_length is None:
            raise ValueError("Start index and burst length must be provided for BURST error")
        return burst_error(codeword, start_index, burst_length)
    else:
        raise ValueError("Invalid error type specified.")