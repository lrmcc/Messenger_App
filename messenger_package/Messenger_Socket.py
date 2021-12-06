#!/usr/bin/env python3

import socket

def get_socket():
    print("Messenger_Socket.get_socket()")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Could not create socket")
        quit()
    return sock

def server_shutdown(srvr, client_dict):
        broadcast_message(client_dict, "server_shutdown")
        broadcast_message(client_dict, "REFUSE")
        srvr.shutdown()
        srvr.close()

def direct_message(sock, message):
    try:
        sock.send(message.encode('ascii'))
    except ConnectionResetError:
        print("direct_message ConnectionResetError")
        pass