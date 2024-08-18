#!/usr/bin/env python3
import sys
import socket
import json
import random
from checksum import generate_checksum_codeword
from crc import generate_crc_codeword
from error_injector import *

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def chunkify(filedata, packet_size, redundant_bits):
    dataword_size = packet_size - redundant_bits
    if dataword_size <= 0:
        print("Packet size must be greater than the number of redundant bits.")
        exit(1)
    return [filedata[i:i + dataword_size] for i in range(0,len(filedata), dataword_size)]

def generate_codeword(dataword, technique):
    if technique == 'checksum':
        return generate_checksum_codeword(dataword)
    elif technique in ['crc-8', 'crc-10', 'crc-16', 'crc-32']:
        return generate_crc_codeword(dataword, technique.upper())
    else:
        raise ValueError("Invalid technique specified")

def manual_error_injection(word):
    error_type = input("Enter error type (MULTI_BIT, BURST, NONE): ").upper()

    if error_type == 'NONE':
        return word, "No Error", None
    if error_type == 'MULTI_BIT':

        indices = [int(i) for i in input("Enter index for MULTI_BIT error separated by comma: ").split(',')]
        if any(index < 0 or index >= len(codeword) for index in indices):
            raise ValueError("Indices out of range")
        infected_codeword = inject_error_manual(word, error_type, indices)
        return infected_codeword, f"Errors in position {indices}", None
    
    elif error_type == 'BURST':
        start_index = int(input("Enter start index for BURST error: "))
        burst_length = int(input("Enter burst length: "))
        infected_codeword = inject_error_manual(word, error_type, start_index=start_index, burst_length=burst_length)
        return infected_codeword, "BURST", burst_length
    else:
        raise ValueError("Invalid error type specified")


def auto_error_injection(codeword):
    error_type = random.choice(['MULTI_BIT', 'BURST', 'NONE'])
    if error_type == 'NONE':
        return codeword, "No Error", None
    elif error_type == 'MULTI_BIT':
        infected_codeword, indices = inject_error_auto(codeword, error_type)
        return infected_codeword, f"Errors in position {indices}", None
    
    if error_type == 'BURST':
        burst_length = random.randint(2, len(codeword))
        infected_codeword = inject_error_auto(codeword, error_type, burst_length)
        return infected_codeword, "BURST", burst_length
    else:
        infected_codeword = inject_error_auto(codeword, error_type)
        return infected_codeword, error_type, None

def send_to_server(s, packet):
    try:
        s.sendall(packet.encode())
        response = s.recv(1024).decode()
        # print('resp: ', response)
        return response
    except (socket.error, socket.timeout) as e:
        print(f"Error during communication with the server: {e}")
        return None


if len(sys.argv) != 6:
    print("Usage: python client.py <port> <file_path> <packet_size> <technique> <error_mode>")
    sys.exit(1)

SERVER_PORT = int(sys.argv[1])
file_path = sys.argv[2]
packet_size = int(sys.argv[3])
technique = sys.argv[4]
error_mode = sys.argv[5]


redundant_bits = {
    'checksum': 16,
    'crc-8': 8,
    'crc-10': 10,
    'crc-16': 16,
    'crc-32': 32
}.get(technique)

if redundant_bits is None:
    print("Invalid technique specified")
    sys.exit(1)

if packet_size <= redundant_bits:
    print("Packet size must be greater than the number of redundant bits.")
    sys.exit(1)

filedata = read_file(file_path)
packets = chunkify(filedata, packet_size, redundant_bits)

print("Packets from file:  ", packets)
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDRESS, SERVER_PORT))

        for index, dataword in enumerate(packets):
            codeword = generate_codeword(dataword, technique)

            if error_mode == 'manual':
                infected_codeword, error_type, burst_length = manual_error_injection(codeword)
            elif error_mode == 'auto':
                infected_codeword, error_type, burst_length = auto_error_injection(codeword)
            else:
                raise ValueError("Invalid error mode specified")

            server_response = send_to_server(s, infected_codeword)
            if server_response is None:
                break

            result = {
                "Packet Index": index,
                "Correct Packet": codeword,
                "Sent Packet": infected_codeword,
                "Error Type": error_type,
                "Accepted/Rejected": server_response
            }
            print(json.dumps(result, indent=4))

        # Close the connection gracefully after sending all packets
        s.shutdown(socket.SHUT_RDWR)
        s.close()
except (socket.error, socket.timeout) as e:
    print(f"Connection error: {e}")