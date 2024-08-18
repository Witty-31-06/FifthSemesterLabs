#!/usr/bin/env python3

import sys
import socket
from checksum import validate_checksum_codeword
from crc import validate_crc_codeword

# Define the server address and port
SERVER_ADDRESS = 'localhost'
# SERVER_PORT = 12345

def check_packet(packet, technique):

    if technique == 'checksum':
        return validate_checksum_codeword(packet)
    elif technique in ['crc-8', 'crc-10', 'crc-16', 'crc-32']:
        return validate_crc_codeword(packet, technique.upper())
    else:
        raise ValueError("Invalid technique specified")


if len(sys.argv) != 3:
    print("Usage: python server.py <port> <technique>")
    sys.exit(1)

technique = sys.argv[2].lower()
SERVER_PORT = int(sys.argv[1])
if SERVER_PORT < 1024 or SERVER_PORT > 65535:
    print("Port number must be between 1024 and 65535")
    sys.exit(1)
if technique not in ['checksum', 'crc-8', 'crc-10', 'crc-16', 'crc-32']:
    print("Invalid technique specified")
    sys.exit(1)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_ADDRESS, SERVER_PORT))
    s.listen()

    print(f"Server is listening on {SERVER_ADDRESS}:{SERVER_PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                is_valid = check_packet(data, technique)
                response = 'ACK' if is_valid else 'NAK'
                conn.sendall(response.encode())
            print(f"Connection closed by {addr}")

