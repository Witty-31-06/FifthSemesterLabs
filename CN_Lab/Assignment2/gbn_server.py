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

config = json.load(open('config.json'))
colors = utils.ANSI_COLOR()
seq_nums = (1 << config['m'])  # Sequence Numbers
Sw = seq_nums - 1  # Sliding Window Size
# Shared resource
Rn = 0
# To ensure order of thread execution
expected_thread_no = 0

# Lock and condition variable to synchronize access to Rn
lock = threading.Lock()
condition = threading.Condition(lock)


SERVER_IP = "127.0.0.1"
PORT = 9999

def handle_request_worker(data, addr, server, delay):
    global Rn
    global expected_thread_no
    data = data.decode()
    is_valid = checksum.validate_checksum_codeword(data)
    if not is_valid:
        print(time.time(), "Checksum validation failed...")
        print(time.time(), f"Current Rn= {Rn}")
        return
    frame_no = frame.Frame.parse_frame(data).frame_no
    threading.current_thread().name = f"{frame_no}"
    print(time.time(), f"Handling Frame {frame_no}...")
    with condition:
        while str(expected_thread_no) != threading.current_thread().name:
            print(time.time(), f"Waiting for thread {expected_thread_no} to finish...")
            condition.wait()
        if frame_no == Rn:
            print(time.time(), f"{colors.ansi_colors[Rn]}Received valid frame {frame_no}")
            Rn = (Rn + 1)%seq_nums
            print(time.time(), f"Incremented Rn to {Rn}")
            if delay > 0:
                print(time.time(), f"{colors.ansi_colors[Rn]}Delaying ACK {Rn} by {delay} seconds...")
                time.sleep(delay)
            server.sendto(str(acknowledgement.ACK(Rn)).encode(), addr)
            print(time.time(), f"ACK#{Rn} sent")
        else:
            print(time.time(), f"Received invalid frame {frame_no}, Rn = {Rn}")
        expected_thread_no = (expected_thread_no + 1)%seq_nums
        condition.notify_all()
        return

        

#UDP Server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((SERVER_IP, PORT))
    server.settimeout(1)
    print(time.time(), f"Server started at {SERVER_IP}:{PORT}")
    while True:
        data = None
        addr = None
        try:
            data, addr = server.recvfrom(1024)
            threading.Thread(target=handle_request_worker, args=(data, addr, server, random.random())).start()
            # print(time.time(), f"Received {data} from {addr}")
        except socket.timeout:
            pass
        time.sleep(0.3)