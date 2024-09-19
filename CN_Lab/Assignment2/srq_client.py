import frame
import socket
import time
import random
import threading
import acknowledgement
from collections import OrderedDict
import utils


lock =  threading.Lock() # Lock used to synchronize updation of ptr1 and pending_frames
colors = utils.ANSI_COLOR()
def readfile(fname):
    with open(fname, "r") as f:
        return f.read()
Sf = 0  # Send Frame Window Start
Sn = 0  # Next Frame to Send
seq_nums = (1 << 5)  # Sequence Numbers
Sw = seq_nums/2  # Sliding Window Size
def break_into_frame(data: str, payload_size: int, window_size:int=1):
    if(payload_size < 46 or payload_size > 1500):
        raise ValueError("Payload size must be between 46 and 1500 bytes")
    frames = []
    cnt = 0
    for i in range(0, len(data), payload_size):
        frames.append(frame.Frame(CLIENT_MAC, SERVER_MAC, data[i:i+payload_size], payload_size, cnt % window_size))
        cnt += 1
    return frames

def inject_random_error(frame: str):
    number_of_errors = random.randint(1, len(frame))
    indices = random.sample(range(len(frame)), number_of_errors)
    f = list(frame)
    for i in indices:
        f[i] = '1' if f[i] == '0' else '0'
    return ''.join(f)


def send_to_server(binary_frame: str, client: socket.socket, server_sock:tuple, reliability_index: float , delay: float):
    # reliability index varies between 0 and 1. 0 means not reliable, 1 means reliable
    frame_no = frame.Frame.parse_frame(binary_frame).frame_no
    if reliability_index < 0 or reliability_index > 1:
        raise ValueError("Reliability index must be between 0 and 1")
    val = random.random()
    msg = f"{colors.ansi_colors[frame_no]}"
    if val > reliability_index:
        msg += f"Error injected in frame {frame_no}...\t"
        binary_frame = inject_random_error(binary_frame)
    if delay > 0:
        msg += f"Delaying {frame_no} by {delay} seconds..."
        print(time.time() ,msg)
        time.sleep(delay)
    client.sendto(binary_frame.encode(), server_sock)
    print(time.time() ,f"{colors.ansi_colors[frame_no]}Frame {frame_no} sent to server...\n")


def handle_ack(ack: str, pending_frames: OrderedDict,ptr1: int, thread_list: list):
    if ack.startswith('ACK'):
        ack_no = acknowledgement.ACK.get_ack_no(ack)
        with lock:
            if (ack_no-1)%seq_nums in pending_frames:
                print(time.time() ,f"{colors.ansi_colors[ack_no]}Received ACK {ack_no}")
                for k, v in pending_frames.copy().items():
                    if k < ack_no:
                        print(f"Deleting {k}")
                        del pending_frames[k]
                        ptr1 += 1
            return ptr1, pending_frames
    else:
        nak_no = acknowledgement.NAK.get_nak_no(ack)
        with lock:
            if nak_no%seq_nums in pending_frames:
                print(time.time() ,f"{colors.ansi_colors[nak_no]}Received NAK {nak_no}")
                #resend that frame
                t = threading.Thread(target=send_to_server, args=(pending_frames[nak_no][0], client, (SERVER_IP, PORT), 0.5, random.random()))
                t.start()
                thread_list.append(t)
                pending_frames[nak_no%seq_nums] = (pending_frames[nak_no][0], time.time(), False)
            return ptr1, pending_frames

SERVER_MAC = "B8:27:EB:3D:3A:3D"
CLIENT_MAC = "B8:27:EB:3D:3A:3D"
PORT = 9999
SERVER_IP = "127.0.0.1"
payload_size = 64
timeout = 2
bitstream = readfile("test.txt")



frames = break_into_frame(bitstream, payload_size, seq_nums)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(0.5)
    ptr1, ptr2 = 0, 0
    n =  len(frames)
    pending_frames = OrderedDict()
    thread_list = []
    while ptr1 < n:
        if ptr2 - ptr1 < Sw and ptr2 < n:
            f = frames[ptr2].frame_to_binary()
            t = threading.Thread(target=send_to_server, args=(f, client, (SERVER_IP, PORT), 0.5, random.random()))
            t.start()
            thread_list.append(t)
            pending_frames[ptr2%seq_nums] = (f, time.time(), False)
            ptr2 += 1
            Sn = ptr2%seq_nums
        for k, v in pending_frames.copy().items():
            if time.time() - v[1] > timeout:
                with lock:
                    print(f"{colors.ansi_colors[k]}Timeout for frame {k}...")
                    t = threading.Thread(target=send_to_server, args=(v[0], client, (SERVER_IP, PORT), 0.5, random.random()))
                    t.start()
                    thread_list.append(t)
                    pending_frames[k] = (v[0], time.time(), False)
        try:
            data, addr = client.recvfrom(1024)
            print(data.decode())
            if data.decode().startswith('ACK') or data.decode().startswith('NAK'):
                ptr1, pending_frames = handle_ack(data.decode(), pending_frames, ptr1, thread_list)
        except socket.timeout:
            pass
        time.sleep(0.5)
    for t in thread_list:
        t.join()
    print("All frames sent successfully...")
                
