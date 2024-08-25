import socket
SERVER_MAC = "00:1A:7D:DA:71:13"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_MAC, 12345))
    s.listen()
    print("Server is listening on port 12345")
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.sendall(data)