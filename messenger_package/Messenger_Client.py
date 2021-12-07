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
        self.USER_ID = hex(get_random_n_digit_int(9))
        self.message_header = ""
        self.last_message_sent = ""

    def start(self):
        try:
            self.USERNAME = input("Enter username: ")
            self.USER_THREAD = threading.Thread(
                target=self.get_user_input, args=(self.SOCKET, self.USERNAME))
            self.RECEIVE_THREAD = threading.Thread(
                target=self.receive_from_server, args=(self.SOCKET, self.USERNAME))
            self.SOCKET.connect(self.ADDRESS)
            connect_message = self.SOCKET.recv(1024).decode('ascii')
            if connect_message == 'INFO':
                info = f"{self.USER_ID}::::{self.USERNAME}"
                self.SOCKET.send(info.encode('ascii'))
                self.RECEIVE_THREAD.start()
                self.USER_THREAD.start()
            else:
                print("Server has not accepted connection")
        except:
            print("Could not start messenger client")
            self.SOCKET.close()
            quit()

    def get_user_input(self, client, username):
        while True:
            try:
                user_input = input("")
                self.message_header = MessengerClient.parse_input(
                    client, self.message_header, user_input)
                message = self.message_header + user_input
                client.send(message.encode('ascii'))
                self.last_message_sent = message
            except:
                break

    def receive_from_server(self, client, username):
        while True:
            try:
                recv_message = client.recv(1024).decode('ascii')
                print(recv_message)
                response = MessengerClient.parse_recieve(
                    client, recv_message, self.last_message_sent)
                if recv_message != response:
                    self.message_header = response
            except:
                print("An exception occurred")
                pass

    @staticmethod
    def parse_recieve(client, recv_message, last_message_sent):
        if recv_message.startswith('DIRECT'):
            print(f"starting direct message with {last_message_sent[2:]}")
            return f"{recv_message[10:]}::::"
        elif recv_message == 'REFUSE' or recv_message == '':
            client.close()
            quit()
        return recv_message

    @staticmethod
    def parse_input(client, message_header, input_message):
        if input_message == "--exit":
            client.close()
            quit()
        elif input_message == '--all':
            return ""
        return message_header
