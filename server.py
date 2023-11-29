import socket
import threading
from random import randint
from helpers import process_player_data

HOST = input('IP address:')
PORT = 12345
MAXSIZE = 1024

class Server:
    def __init__(self):
        self.pos = {}
        self.colors = {}
        self.foodpos = [0, 0]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print('listening')
        while True:
            conn, addr = self.socket.accept()
            print('connected')
            threading.Thread(target=self.player_handler, args=[conn]).start()


    def player_handler(self, conn):
        print('player handler')

        fd = conn.fileno()
        while True:
            data = conn.recv(MAXSIZE).decode()
            print(data)
            if data == 'quit': 
                del self.pos[fd]
                return
            
            if data == 'food eaten': 
                self.foodpos = [randint(0, 17) * 50 for _ in range(2)]
            else:            
                data = data.split(' ')
                self.pos[fd], self.colors[fd] = process_player_data(data)
                res = f'food {self.foodpos[0]} {self.foodpos[1]},'
                for player in self.pos: 
                    if player != fd: 
                        res += f'{player} '
                        for x, y in self.pos[player]: res += f'{x} {y} '
                        res += f'{self.colors[player]},'

                if not res: res = '-'
                print(str.encode(res))
                conn.send(str.encode(res))
                print('sent')

s = Server()

