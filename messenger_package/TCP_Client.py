#!/usr/bin/env python3

import socket
import random
import time

class TCPClient():
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.MESSAGE_LOG = []
        self.set_client_id()

    def set_client_id(self):
        random.seed(time.time_ns())
        self.client_id = hex(int(round(((random.random()) * 1000000000),0)))
    
    def get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_connect(self, sock):
        sock.connect((self.HOST,self.PORT)) 

    def socket_sendall(self, sock):
        sock.sendall(bytes(self.message, 'ascii'))

    def socket_response(self, sock):
        self.response = str(sock.recv(1024), 'ascii')

    def get_user_message(self):
        self.message = input(">: ")
    
    def add_message_header(self, header):
        self.message = f"{header}:{self.message}"

    def send_message_with_socket(self):
        with self.get_socket() as sock:
            self.socket_connect(sock)
            self.socket_sendall(sock)
            self.socket_response(sock)
            print(f"Server echo: {self.response}")

    def run(self):
        self.connect()
        while(self.client_run):
            self.get_user_message()
            if self.message == 'exit': self.disconnect()
            self.MESSAGE_LOG.append(self.message)
            self.send_message_with_socket()

    def connect(self):
        self.client_run = True
        self.message = f"CONNECT::::{self.client_id}"
        self.send_message_with_socket()
     
    def disconnect(self):
        self.client_run = False
        self.message = f"DISCONNECT::::{self.client_id}"
