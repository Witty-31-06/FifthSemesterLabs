import socket
import sys
import frame
import random
import time
CLIENT_MAC =  "00:1A:7D:DA:80:13"
port = sys.argv[1]
SERVER_MAC = "00:1A:7D:DA:71:13"

def break_into_frame(data, payload_size, window_size=1):
    if(payload_size < 46 or payload_size > 1500):
        raise ValueError("Payload size must be between 46 and 1500 bytes")
    frames = []
    for i in range(0, len(data), payload_size):
        frames.append(frame.Frame(CLIENT_MAC, SERVER_MAC, data[i:i+payload_size], payload_size, i%window_size))
    return frames


def send_to_server(frame, reliability=1, delay=0):
    frame_copy = frame
    p = random.uniform(0, 1-reliability) # probability of error (reliability of the channel)

    for i in range(len(frame_copy.data)):
        if random.uniform(0, 1) < p:
            #flip bit (binary string)
            frame_copy.data[i] = '1' if frame_copy.data[i] == '0' else '0'
    
    #introduce delay
    time.sleep(random.uniform(0, delay))
    clientsock.send(frame_copy.frame_to_binary().encode())
    server_response = clientsock.recv(1024) #NAK or ACK



clientsock  = socket.socket()
clientsock.connect((SERVER_MAC, int(port)))

data = open('test.txt', 'r').read()
frames = break_into_frame(data, 100)
index = 0
while True:
    if index >= len(frames):
        break
    bin_data = frames[index].frame_to_binary()
    send_to_server(bin_data)
    index += 1
    print(f"Sent frame {index}")

