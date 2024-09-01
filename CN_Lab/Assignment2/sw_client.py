import frame
import socket
import time
import random
import threading
import acknowledgement
import utils
import json

config = json.load(open("config.json"))
colors = utils.ANSI_COLOR()
def readfile(fname):
    with open(fname, "r") as f:
        return f.read()

def break_into_frame(data: str, payload_size: int, window_size:int = 2 ):
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

def send_to_server(idx: int, client: socket.socket, server_sock:tuple, reliability_index: float , delay: float):
    # reliability index varies between 0 and 1. 0 means not reliable, 1 means reliable
    binary_frame = frames[idx].frame_to_binary()
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
    try:
        client.sendto(binary_frame.encode(), server_sock)
        print(time.time() ,f"{colors.ansi_colors[frame_no]}Frame {frame_no} sent to server...\n")
    except socket.timeout:
        pass
    

SERVER_MAC = "B8:27:EB:3D:3A:3D"
CLIENT_MAC = "B8:27:EB:3D:3A:3D"
PORT = 9999
SERVER_IP = "127.0.0.1"
payload_size = 64
timeout = config['timeout']
bitstream = readfile("test.txt")

recv_intr = threading.Event()
ack = ''
all_sent = False
def recv(client: socket.socket):
    global recv_intr
    global ack
    while True and all_sent == False:
        while not recv_intr.is_set() and all_sent == False:
            try:
                data, addr = client.recvfrom(1024)
                print(time.time() ,f"Received ACK {data.decode()}")
                ack = data.decode()
                recv_intr.set()
            except socket.timeout:
                pass

def handle_ack(Sn: int, idx:int):
    recv_intr.clear()
    if acknowledgement.ACK.get_ack_no(ack) == Sn:
        idx = (idx + 1)
        Sn = (Sn + 1)%2
    return idx, Sn

frames = break_into_frame(bitstream, payload_size, window_size=2)
Sn = 0
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(1)
    server_sock = (SERVER_IP, PORT)
    idx = 0
    n = len(frames)
    t =  threading.Thread(target=recv, args=(client,))
    t.start()
    can_send = True
    while idx < n:
        
        if can_send:
            print(idx, all_sent)
            threading.Thread(target=send_to_server, args=(idx, client, server_sock, 0.9, 0.1)).start()
            Sn = (Sn + 1)%2
            can_send = False
            recv_intr.wait(timeout)
        if recv_intr.is_set():
            idx, Sn = handle_ack(Sn, idx)
            can_send = True
        else:
            print(time.time(), f"Timeout for frame {idx}")
            can_send = True
        if idx == n:
            all_sent = True
        time.sleep(0.3)
    t.join()
        
