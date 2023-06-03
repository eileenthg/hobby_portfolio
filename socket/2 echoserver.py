import socket

host = '127.0.0.1'
port = 65432 #note: non-priviledged ports are >1023, 0 is reserved, max is 65535)

print("Running...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Sending back:', data)
            conn.sendall(data)

print('Client connection closed.')