#!/usr/bin/env python3

import threading
import getpass

from messenger_package.Messenger_Socket import *
from messenger_package.Messenger_Functions import *


class MessengerClient():
    def __init__(self, address):
        self.ADDRESS = address
        self.USER = getpass.getuser()
        self.SOCKET = get_socket()
        self.USER_ID= hex(get_random_n_digit_int(9))
        self.last_message_sent = ""
        self.direct_message_mode = False

    def start(self):
        try:
            self.USERNAME = input("Enter username: ")
            self.USER_THREAD = threading.Thread(target=self.get_user_input, args=(self.SOCKET, self.USERNAME))
            self.RECEIVE_THREAD = threading.Thread(target=self.receive_from_server, args=(self.SOCKET, self.USERNAME))
            self.SOCKET.connect(self.ADDRESS)
            connect_message = self.SOCKET.recv(1024).decode('ascii')
            if connect_message == 'INFO':
                info = f"{self.USER_ID}::::{self.USERNAME}"
                self.SOCKET.send(info.encode('ascii'))
                print(f"client info sent to server: {info}")
                self.USER_THREAD.start()
                self.RECEIVE_THREAD.start()
            else: 
                print("Server has not accepted connection")
        except:
            print("Could not start messenger client")
            self.SOCKET.close()
            quit()

    def get_user_input(self, client, username):
        while True:
            try:
                if self.direct_message_mode:
                    msg = MessengerClient.parse_input(client, input(f'\nTo {self.direct_target_name} >: '), False)
                    message =(f"{self.direct_target_name}::::From {username}: {msg}")
                    client.send(message.encode('ascii'))
                    self.last_message_sent = message
                else:
                    user_input = input("")
                    message = MessengerClient.parse_input(client, user_input, False)
                    client.send(message.encode('ascii'))
                    self.last_message_sent = message
            except:
                break

    def receive_from_server(self, client, username):
        while True:
            try:
                recv_message = client.recv(1024).decode('ascii')
                print(f"recv_message = client.recv(1024).decode('ascii'). where recv_message: {recv_message}")
                response = MessengerClient.parse_recieve(client, username, recv_message, self.last_message_sent)
                if len(response) > 0:
                    client.send(response.encode('ascii'))
                    self.last_message_sent = response
            except:
                break

    def direct_message_manager(self, status, name, target):
        self.direct_message_mode = status
        self.direct_target_name = name
        self.direct_target_client_id = target

    @staticmethod
    def parse_recieve(client, recv_message, last_message_sent):
        print("parse_recieve")
        if recv_message.startswith('DIRECT'):
            MessengerClient.direct_message_manager(True, last_message_sent[2:], recv_message[10:]) 
        elif recv_message == 'REFUSE' or recv_message == '':
            client.close()
            quit()
        return recv_message

    @staticmethod
    def parse_input(client, input_message, direct_message_mode):
        if input_message == "--exit":
            client.send(input_message.encode('ascii'))
            client.close()
            quit()
        elif input_message == '--all' and direct_message_mode:
            MessengerClient.direct_message_manager(False, "", "")
        return input_message