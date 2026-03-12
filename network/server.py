import socket
import threading
# import struct

HOST = "127.0.0.1"
PORT = 8989

def start_server():
    # Open server and wait for client
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("listening..")

    player1, _ = server.accept()
    print("player 1 connected")
    
    player2, _ = server.accept()
    print("player 2 connected")

    threading.Thread(target=create_tunnel, args=(player1, player2)).start()
    threading.Thread(target=create_tunnel, args=(player2, player1)).start()


def create_tunnel(sender : socket.socket, reciever : socket.socket):
    while True:
        reciever.send(sender.recv(13))



start_server()























    # while True:
    #     # +--------------------------------+
    #     # |            PROTOCOL            |
    #     # |--------------------------------|
    #     # |  x (4 bytes)  |  y (4 bytes)   |
    #     # |--------------------------------|
    #     # | dir (4 bytes) | shoot (1 byte) |
    #     # +--------------------------------+
    #     package = client.recv(13)
    #     # x, y, dir, shoot = struct.unpack("iif?", package)
    #     yield struct.unpack("iif?", package)




# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen(1)
# print("listening..")
# client, addr = server.accept()

# print(f"hi client from {addr}")

