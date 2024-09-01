import frame
import socket
import time
import random
import threading
import acknowledgement
import collections
import utils


lock =  threading.Lock() # Lock used to synchronize updation of ptr1 and pending_frames
colors = utils.ANSI_COLOR()
def readfile(fname):
    with open(fname, "r") as f:
        return f.read()
Sf = 0  # Send Frame Window Start
Sn = 0  # Next Frame to Send
seq_nums = (1 << 2)  # Sequence Numbers
Sw = seq_nums - 1  # Sliding Window Size
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

def handle_ack(ack: str, pending_frames: dict, ptr1: int):
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
        
SERVER_MAC = "B8:27:EB:3D:3A:3D"
CLIENT_MAC = "B8:27:EB:3D:3A:3D"
PORT = 9999
SERVER_IP = "127.0.0.1"
payload_size = 64
timeout = 2
bitstream = readfile("test.txt")



frames = break_into_frame(bitstream, payload_size, seq_nums)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(1)
    ptr1, ptr2 = 0, 0
    n =  len(frames)
    pending_frames = collections.OrderedDict()
    thread_list = []
    while ptr1 < n:
        print(f"ptr1= {ptr1}, ptr2= {ptr2}")
        for k, v in pending_frames.items():
            print(f'{k}: {v[1]}')
        if ptr2 - ptr1 < Sw:
            if ptr2 < n:
                f = frames[ptr2].frame_to_binary()
                t = threading.Thread(target=send_to_server, args=(f, client, (SERVER_IP, PORT), 0.9, random.random()))
                t.start()
                thread_list.append(t)
                pending_frames[ptr2%seq_nums] = (f, time.time())
                ptr2 += 1
                Sn = ptr2%seq_nums
        #Check if first frame in dictionary has timed out
        if len(pending_frames) > 0:
            if time.time() - pending_frames.get(ptr1%seq_nums)[1] > timeout:
                print(time.time() ,f"{colors.ansi_colors[ptr1%seq_nums]}Timeout for frame {ptr1%seq_nums}")
                #clear entire dictionary and resend entire window
                with lock:
                    temp = collections.OrderedDict()
                    thread_list.clear()
                    for k, v in pending_frames.items():
                        f = v[0]
                        t = threading.Thread(target=send_to_server, args=(f, client, (SERVER_IP, PORT), 0.9, random.random()))
                        t.start()
                        thread_list.append(t)
                        temp[k] = (v[0], time.time())

                    pending_frames = temp


        try:
            data, addr = client.recvfrom(1024)
            print(data.decode())
            if data.decode().startswith('ACK'):
                # ack_th = myThread(target=handle_ack, args =(data.decode(), pending_frames, ptr1))
                # ack_th.start()
                # ptr1, pending_frames = ack_th.join()
                ptr1, pending_frames = handle_ack(data.decode(), pending_frames, ptr1)
                Sf = ptr1%seq_nums
        except socket.timeout:
            pass
        time.sleep(0.5)
    for t in thread_list:
        t.join()
    print(time.time() ,"All frames sent successfully...")