import socket

host = '127.0.0.1' #server ip
port = 65432 #server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while True:
        send = input('->')
        if not send:
            break
        s.sendall(send.encode())
        data = s.recv(1024)
        print('Received:', data.decode())

print('Connection closed.')
