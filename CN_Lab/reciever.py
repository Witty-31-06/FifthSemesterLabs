import socket
import Checksum
import CRC

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 9999))
s.listen(1)

print("Waiting for connection...")
while True:
    conn, addr = s.accept()
    print("Connected to", addr)
    method = conn.recv(1024).decode()
    #first thing recieved is method
    code = conn.recv(1024).decode() #checksum/divisor
    print("Method:", method)
    lis = []
    while True:
        data = conn.recv(1024).decode()
        if data == 'EOF':
            break
        lis.append(data)
    text = ''.join(lis)
    print("Data recieved:", text)
    if method == 'CRC':
        if CRC.CRC.checkRemainder(text, code):
            print("Remainder is 0")
            conn.send(b'ACK')
        else:
            conn.send(b'NAK')
    elif method == 'Checksum':
        if Checksum.Checksum.check_checksum(text, code):

            conn.send(b'ACK')
        else:
            conn.send(b'NAK')
    else:
        print("Invalid method")
        conn.close()
    conn.close()
