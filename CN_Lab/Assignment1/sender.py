#Simulate error correction protocols using socket programming


import random
import time
import socket
import CRC
import Checksum

HOST = 'localhost'
PORT = 9999
PKT_SIZE = 8
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
random.seed(time.time())

def inject_error(text, number):
    if number == 0:
        return text
    #text is binary string
    for _ in range(number):
        pos = random.randint(0, len(text)-1)
        text = text[:pos] + ('1' if text[pos] == '0' else '0') + text[pos+1:]
    return text

s.connect((HOST, PORT))
f = open('data.txt', 'r')
data = f.read()
f.close()
nums = input("Want to inject errors?: ")
method = input("Enter the method you want to use (CRC or Checksum): ")

datalen = len(data)
if(datalen%PKT_SIZE != 0):
    data += '0'*(PKT_SIZE - datalen%PKT_SIZE) #Padding by 0
datalen = len(data)

packets = [data[i:i+PKT_SIZE] for i in range(0, datalen, PKT_SIZE)]

# s.sendall()

if method == 'CRC':
    s.send(b'CRC')
    time.sleep(1)
    print("1. CRC-8: x^8 + x^2 + x + 1")
    print("2. CRC-16: x^16 + x^15 + x^2 + 1")
    print("3. CRC-10: x^10 + x^9 + x^5 + x^4 + x + 1")
    print("4. CRC-32: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1")
    poly = input("Enter the polynomial you want to use: ")
    divisor = CRC.CRC.polyToBin(poly)
    s.send(divisor.encode())
    packets = CRC.CRC.encodeData(packets, divisor)
elif method == 'Checksum':
    s.send(b'Checksum')
    time.sleep(1)
    s.send(Checksum.Checksum.generate_checksum(packets).encode())
else:
    print("Invalid method")
    s.close()
    exit()

#send packets
good_packet = packets.copy()
for i in range(len(packets)):
    if nums == 'y':
        packets[i] = inject_error(packets[i], random.randint(0, 3))
    s.send(packets[i].encode())
s.send(b'EOF')
print("Data sent:", packets)
print(good_packet)
print(s.recv(1024).decode())
s.close()