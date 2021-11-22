#!/usr/bin/env python3

import socketserver
import socket
import threading
import time
import re

class MessengerServer():
    def __init__(self, address, encoding):
        self.HOST, self.PORT = address
        self.ENCODING = encoding
        self.client_dict = {}

    def start(self):
        try:
            self.server_setup()
            self.server_run()
        except:
            print("Could not start server")
            exit(0)

    def server_setup(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        self.SERVER_STATUS = True

    def server_run(self):
        with self.server:
            while (self.SERVER_STATUS):
                try:
                    self.accept_client()
                except:
                    pass
        self.server_shutdown()

    def server_shutdown(self):
        self.broadcast_message("server_shutdown")
        self.broadcast_message("REFUSE")
        self.client_dict.clear()
        self.SERVER_STATUS = False
        self.server.shutdown()

    def accept_client(self):
        client, address = self.server.accept()
        try:
            self.direct_message(client, 'INFO')
            client_info = client.recv(1024).decode(self.ENCODING)
            self.add_client(client, address, client_info)
        except ConnectionResetError:
            print("ConnectionResetError")
            return
        
        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

    def handle(self, client):
        client_connected_flag = True
        while client_connected_flag:
            try:
                recv_message = client.recv(1024).decode(self.ENCODING)
                if recv_message.startswith('--'):
                    client_connected_flag = self.parse_command(client, recv_message[2:])
                elif "::::" in recv_message:
                    target_client_id, message = recv_message.split("::::", 1)
                    target_client = self.get_client_by_client_id(target_client_id)
                    self.direct_message(target_client, message)
                else:
                    message = f"{self.client_dict[client][1]}: {recv_message}"
                    self.broadcast_message(message)
            except ConnectionResetError:
                self.remove_client(client)
                break
        if (not self.SERVER_STATUS):
            self.server.close()
        return
                
    def direct_message(self, client, message):
        print("direct_message(self, client, message)")
        try:
           client.send(message.encode(self.ENCODING))
        except ConnectionResetError:
            print("direct_message ConnectionResetError")
            pass
        
    def broadcast_message(self, message):
        for key in self.client_dict:
            try:
                key.send(message.encode(self.ENCODING))
            except ConnectionResetError:
                print("broadcast_message ConnectionResetError for particular client")
                continue
    
    def add_client(self, client, address, client_info):
        client_id, username = client_info.split("::::", 1)
        self.client_dict[client] = [client_id, username, address]
        self.broadcast_message(f'{username} joined the chat from {address}')
   
    def remove_client(self, client):
        self.broadcast_message(f"{self.client_dict[client][1]} left the chat!")
        del self.client_dict[client]
    
    def get_client_by_client_id(self, client_id):
        for key, value in self.client_dict.items():
            if value[0] == client_id:
                return key
        return None
    
    def get_client_id_by_username(self, username):
        for key, value in self.client_dict.items():
            if value[1] == username:
                return value[0]
        return None
    
    def get_usernames_list(self):
        client_list = []
        for val in list(self.client_dict.values()):
            client_list.append(val[1])
        return client_list
    
    def get_all_usernames_str(self):
        ret_string = ', '.join(str(val) for val in self.get_usernames_list())
        return f"Connected users: {ret_string}"

    def parse_command(self, client, command):
        if command == "users":
            self.direct_message(client, self.get_all_usernames_str())
        elif command in self.get_usernames_list():
            target_client_id = self.get_client_id_by_username(command)
            if target_client_id == None:
                self.direct_message(client, f"Direct message target user unavailable")
            else:
                self.direct_message(client, f"DIRECT::::{target_client_id}")
        elif command == "exit":
            self.remove_client(client)
            return False
        elif command == "shutdown":
            self.server_shutdown()
            return False
        else:
            self.direct_message(client, f"{command} is an invalid command")
        return True