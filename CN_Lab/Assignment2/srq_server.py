import frame
import checksum
import socket
import time
import threading
import random
import threading
import acknowledgement
import utils
import json
from collections import OrderedDict
config = json.load(open('config.json'))
colors = utils.ANSI_COLOR()
seq_nums = (1 << config['m'])  # Sequence Numbers
Sw = seq_nums//2  # Sliding Window Size
# Shared resource
Rn = 0

# To ensure order of thread execution
expected_thread_no = 0
nakSent = False
ackNeeded = True
marked = [False for i in range(Sw)]
final_dict = OrderedDict()
temp_dict = OrderedDict()
# Lock and condition variable to synchronize access to Rn
lock = threading.Lock()
condition = threading.Condition(lock)


SERVER_IP = "127.0.0.1"
PORT = 9999

def handle_request_worker(data, addr, server):
    q = random.random()
    global Rn
    global marked
    global final_dict
    global nakSent
    global ackNeeded
    global temp_dict
    data = data.decode()
    is_valid = checksum.validate_checksum_codeword(data)
    if not is_valid and nakSent == False:
        print(time.time(), "Checksum validation failed...")
        print(time.time(), f"Current Rn= {Rn}")
        if q > 0.5:
            print(time.time(), f"NAK#{Rn} lost")
            return
        server.sendto(str(acknowledgement.NAK(Rn)).encode(), addr)
        print(time.time(), f"NAK#{Rn} sent")
        nakSent = True
        return
    f = frame.Frame.parse_frame(data)
    frame_no = f.frame_no
    if frame_no != Rn and nakSent == False:
        print(f"Expected frame {Rn}")
        if q > 0.5:
            print(time.time(), f"NAK#{Rn} lost")
            return
        server.sendto(str(acknowledgement.NAK(Rn)).encode(), addr)
        print(time.time(), f"NAK#{Rn} sent")
        nakSent = True
    elif frame_no in range(Rn, Rn+Sw) and marked[frame_no] == False:
        marked[frame_no] = True
        temp_dict[frame_no] = f
        while marked[Rn]:
            final_dict[Rn] = temp_dict[Rn]
            del temp_dict[Rn]
            Rn = Rn+1
            ackNeeded = True
        if ackNeeded:
            print(f"ACK#{Rn} sent...")
            server.sendto(str(acknowledgement.ACK(Rn)).encode(), addr)
            nakSent = False
            ackNeeded = False



        

#UDP Server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((SERVER_IP, PORT))
    server.settimeout(0.5)
    print(time.time(), f"Server started at {SERVER_IP}:{PORT}")
    while True:
        data = None
        addr = None
        try:
            data, addr = server.recvfrom(1024)
            handle_request_worker(data, addr, server)
        except socket.timeout:
            pass
        time.sleep(0.3)