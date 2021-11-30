#!/usr/bin/env python3

import socket
import random
import time
import threading
import getpass

class MessengerClient():
    def __init__(self, address):
        self.HOST, self.PORT = address
        self.USER = getpass.getuser()
        self.CLIENT = MessengerClient.client_socket_setup(address)
        self.USERNAME = input("Enter username: ")
        self.message = ""
        self.USER_THREAD = threading.Thread(target=self.get_user_input, args=(self.CLIENT, self.USERNAME, self.message))
        self.RECEIVE_THREAD = threading.Thread(target=self.receive_from_server, args=(self.CLIENT, self.USERNAME))
        self.direct_message_mode = False

    def start(self):
        try:
            print("try thread.start()")
            self.USER_THREAD.start()
            self.RECEIVE_THREAD.start()
        except:
            print("Could not start threads")
            MessengerClient.client_socket_shutdown(self.CLIENT)

    def get_user_input(self, client, username, message):
        print("get_user_input()")
        while True:
            try:
                if self.direct_message_mode:
                    print("get_user_input, while True: try: if self.direct_message_mode:")
                    msg = MessengerClient.parse_input(client, input(f'\nTo {self.direct_target_name} >: '), False)
                    print("if self.direct_message_mode: msg = MessengerClient.parse_input")
                    message =(f"{self.direct_target_name}::::From {username}: {msg}")
                    MessengerClient.send_to_server(client, message)
                    print("get_user_input, if self.direct_message_mode: send_to_server")
                else:
                    print("get_user_input, while True: try: else:")
                    user_input = input("")
                    print(f"user_input = {user_input}")
                    message = MessengerClient.parse_input(client, user_input, False)
                    print(f"message = {message}")
                    MessengerClient.send_to_server(client, message)
                    print("get_user_input, try else: send_to_server")
            except:
                break

    def receive_from_server(self, client, username):
        print("receive_from_server()")
        while True:
            try:
                print("receive_from_server() while True: try:")
                recv_message = client.recv(1024).decode('ascii')
                print(f"recv_message: {recv_message}")
                response = self.parse_recieve(client, username, recv_message)
                print(f"receive_from_server(), response = {response}")
                if len(response) > 0:
                    MessengerClient.send_to_server(client, response)
                    print(f"receive_from_server, send_to_server just sent: {response}")
            except:
                break

    def direct_message_manager(self, status, name, target):
        self.direct_message_mode = status
        self.direct_target_name = name
        self.direct_target_client_id = target

    
    def parse_recieve(self, client, username, recv_message):
        print(f"parse_recieve: {recv_message}")
        if recv_message == 'INFO':
            print(f"parse_recieve(), if recv_message == 'INFO':")
            client_id = MessengerClient.get_client_id()
            info = f"{client_id}::::{username}"
            print(f"info: {info}")
            return str(info)
        elif recv_message.startswith('DIRECT'):
            message = self.get_message()
            MessengerClient.direct_message_manager(True, message[2:], recv_message[10:])
            return ""
        elif recv_message == 'REFUSE' or recv_message == '':
            MessengerClient.client_socket_shutdown(client)
        else:
            return "" # recv_message

    def get_message(self):
        return self.message

    @staticmethod
    def parse_input(client, input_message, direct_message_mode):
        print(f"parse_input {input_message}")
        if input_message == "--exit":
            MessengerClient.send_to_server(input_message)
            MessengerClient.client_socket_shutdown(client)
        elif input_message == '--all' and direct_message_mode:
            MessengerClient.direct_message_manager(False, "", "")
            return "private chat ended"
        else:
            return input_message

    @staticmethod
    def client_socket_setup(address):
        host, port = address
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
        except:
            print("Could not create client socket")
            MessengerClient.client_socket_shutdown(client)
        return client
    
    @staticmethod
    def client_socket_shutdown(client):
        client.close()
        exit(0)

    @staticmethod
    def send_to_server(client, message):
        print(f"about to send_to_server: {message}")
        client.send(message.encode('ascii'))
        print(f"send_to_server successfully sent: {message}")
        
    @staticmethod
    def get_client_id():
        print("in get_client_id()")
        random.seed(time.time_ns())
        return hex(int(round(((random.random()) * 1000000000),0)))