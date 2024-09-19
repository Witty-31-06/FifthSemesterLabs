import socket
import time
with socket.socket() as s:
    s.connect(('127.0.0.1', 10000))
    s.sendall(b'Hello, world')
    s.sendall(b'Hello, world')
    s.sendall(b'Hello, world')
    time.sleep(10)