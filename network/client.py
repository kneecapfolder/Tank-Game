import socket
import struct
from game.tank import Tank


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binding_data = (host, port)


    def connect_to_server(self):
        self.sock.connect(self.binding_data)

    
    # +--------------------------------+
    # |            PROTOCOL            |
    # |--------------------------------|
    # |  x (4 bytes)  |  y (4 bytes)   |
    # |--------------------------------|
    # | dir (4 bytes) | shoot (1 byte) |
    # +--------------------------------+

    def send_data(self, player : Tank, shoot : bool):
        self.sock.send(struct.pack('iif?', int(player.x), int(player.y), player.dir, shoot))


    async def get_enemy_data(self):
        while True:
            yield struct.unpack("iif?", self.sock.recv(13))