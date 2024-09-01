import frame
import socket
import time
import random
import threading
import acknowledgement
import utils
import json
import checksum

SERVER_IP = "127.0.0.1"
PORT = 9999
Rn = 0
config = json.load(open("config.json"))
colors = utils.ANSI_COLOR()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((SERVER_IP, PORT))
    server.settimeout(1)
    print(time.time(), f"Server started at {SERVER_IP}:{PORT}")
    while True:
        data = None
        addr = None
        try:
            data, addr = server.recvfrom(1024)
            data = data.decode()
            if checksum.validate_checksum_codeword(data):
                frame_no = frame.Frame.parse_frame(data).frame_no
                print(time.time(), f"{colors.ansi_colors[frame_no]}Rn: {Rn} Frame {frame_no} received from client...")
                if frame_no == Rn:
                    Rn = (Rn + 1)%2
                p = random.random()
                q = random.random()
                if q < p and q > 0.01:
                    time.sleep(q)
                    print(time.time(), f"ACK#{Rn} delayed {q}...")
                server.sendto(str(acknowledgement.ACK(Rn)).encode(), addr)
                print(time.time(), f"ACK#{Rn} sent to client...")
            else:
                print(f"Recieved corrupted frame. Rn: {Rn}")
        except socket.timeout:
            pass
