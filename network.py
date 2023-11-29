import socket

HOST = input('IP address:')
PORT = 12345
MAXSIZE = 1024

class Network:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

    def send(self, data, response=True):
        print(data)
        self.socket.send(str.encode(data))
        if response: return self.socket.recv(MAXSIZE).decode()
        else: return None
