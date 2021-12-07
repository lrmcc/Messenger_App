#!/usr/bin/env python3

import threading

from messenger_package.Messenger_Socket import *
from messenger_package.Messenger_Functions import *


class MessengerServer():
    def __init__(self, address):
        self.ADDRESS = address
        self.SOCKET = get_socket()
        self.client_dict = {}

    def start(self):
        try:
            self.SOCKET.bind(self.ADDRESS)
            self.SOCKET.listen()
            self.SERVER_STATUS = True
            with self.SOCKET:
                while (self.SERVER_STATUS):
                    try:
                        self.accept_client()
                    except:
                        pass
            server_shutdown(self.SOCKET, self.client_dict)
        except:
            print("Could not start server")
            exit(0)

    def accept_client(self):
        client, address = self.SOCKET.accept()
        try:
            direct_message(client, 'INFO')
            client_info = client.recv(1024).decode('ascii')
            client_id, username = client_info.split("::::", 1)
            self.client_dict[client] = [client_id, username, address]
            msg = f'{username} joined the chat from {address}'
            broadcast_message(self.client_dict, msg)
        except ConnectionResetError:
            print("ConnectionResetError")
            return
        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

    def handle(self, client):
        client_connected_flag = True
        while client_connected_flag:
            try:
                recv_message = client.recv(1024).decode('ascii')
                if recv_message.startswith('--'):
                    client_connected_flag = MessengerServer.parse_command(
                        client, self.client_dict, recv_message[2:])
                elif "::::" in recv_message:
                    target_client_id, message = recv_message.split("::::", 1)
                    target_client = get_key_by_dict_val_x(
                        self.client_dict, target_client_id, 0)
                    direct_message(target_client, message)
                else:
                    message = f"{self.client_dict[client][1]}: {recv_message}"
                    broadcast_message(self.client_dict, message)
            except ConnectionResetError:
                broadcast_message(
                    self.client_dict, f"{self.client_dict[client][1]} left the chat!")
                del self.client_dict[client]
                break
        if (not self.SERVER_STATUS):
            self.client_dict.clear()
            server_shutdown(self.SOCKET, self.client_dict)
            self.SERVER_STATUS = False
            quit()
        return

    @staticmethod
    def parse_command(client, client_dict, command):
        if command == "users":
            direct_message(client, get_str_all_val_x(client_dict, 1))
        elif command == "all":
            direct_message(client, get_str_all_val_x(client_dict, 1))
        elif command in get_list_of_dict_idx_x(client_dict, 1):
            target_client_id = get_dict_value_x_by_value_y(
                client_dict, command, 0, 1)
            if target_client_id == None:
                direct_message(
                    client, f"Direct message target user unavailable")
            else:
                direct_message(client, f"DIRECT::::{target_client_id}")
        elif command == "exit":
            broadcast_message(
                client_dict, f"{client_dict[client][1]} left the chat!")
            del client_dict[client]
            return False
        elif command == "shutdown":
            server_shutdown(client, client_dict)
            return False
        else:
            direct_message(client, f"{command} is an invalid command")
        return True
