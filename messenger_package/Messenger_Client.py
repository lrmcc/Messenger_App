#!/usr/bin/env python3

import socket
import random
import time
import threading
import getpass

class MessengerClient():
    def __init__(self, address, encoding):
        self.HOST, self.PORT = address
        print(f"self.HOST: {self.HOST} self.PORT: {self.PORT}")
        self.ENCODING = encoding
        self.USER = getpass.getuser()
        self.CLIENT_ID = MessengerClient.get_client_id()
        self.RECEIVE_THREAD = threading.Thread(target=self.receive_from_server)
        self.USER_THREAD = threading.Thread(target=self.get_user_input)

    def start(self):
        self.USERNAME = input("Enter username: ")
        self.direct_message_mode = False
        self.direct_message_target = ""
        self.client_socket_setup()
        if (self.client_run): self.thread_start()

    def client_socket_setup(self):
        try:
            self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.CLIENT.connect((self.HOST, self.PORT))
            self.client_run = True
        except:
            print("Could not create client socket")
            self.client_socket_shutdown()

    def thread_start(self):
        print("thread_start")
        try:
            self.RECEIVE_THREAD.start()
            self.USER_THREAD.start()
        except:
            print("Could not start threads")
            self.client_socket_shutdown()

    def get_user_input(self):
        while self.client_run:
            if self.direct_message_mode:
                self.direct_message()
            else:
                self.broadcast_message()

    def receive_from_server(self):
        while self.client_run:
            try:
                self.recv_message = self.CLIENT.recv(1024).decode('ascii')
                self.parse_recieve()
            except:
                break

    def parse_input(self):
        if self.message == "--exit":
            self.send_to_server(self.message)
            self.client_socket_shutdown()
        if self.message == '--all' and self.direct_message_mode:
            self.direct_message_manager(False, self.message[2:], self.recv_message[10:])
            self.message = "private chat ended"
    
    def parse_recieve(self):
        print(f"parse_recieve self.recv_message: {self.recv_message }")
        if self.recv_message == 'INFO':
            self.send_to_server(f"{self.CLIENT_ID}::::{self.USERNAME}")
        elif self.recv_message.startswith('DIRECT'):
            self.direct_message_manager(True, self.message[2:], self.recv_message[10:])
        elif self.recv_message == 'REFUSE':
            self.client_socket_shutdown()
        elif self.recv_message == '':
            self.client_socket_shutdown()
        else:
            print(self.recv_message)
    
    def broadcast_message(self):
        self.message = input("\nTo all >:")
        self.parse_input()
        self.send_to_server(self.message)

    def direct_message(self):
        self.message = input(f'\nTo {self.direct_message_name} >: ')
        self.parse_input()
        self.message =(f"{self.direct_message_target}::::From {self.USERNAME}: {self.message}")
        self.send_to_server(self.message)
        
    def direct_message_manager(self, status, name, target):
        self.direct_message_mode = status
        self.direct_message_name = name
        self.direct_message_target = target
            
    def client_socket_shutdown(self):
        self.CLIENT.close()
        self.client_run = False
        exit(0)

    def send_to_server(self, message):
        self.CLIENT.send(message.encode(self.ENCODING))
        
    @staticmethod
    def get_client_id():
        random.seed(time.time_ns())
        return hex(int(round(((random.random()) * 1000000000),0)))

    @staticmethod
    def toggle(toggle_target):
        print("inside toggle")
        if toggle_target:
            return False
        else:
            return True
