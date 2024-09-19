import time
import socket
with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 10000))
    s.listen()
    conn, addr =  s.accept()
    print(f"Connected to {addr}")
    while True:
        time.sleep(5)
        data = conn.recv(1024)
        print(data)
        