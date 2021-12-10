import threading

from messenger_package.Messenger_Socket import *
from messenger_package.Messenger_Functions import *


class MessengerServer():
    def __init__(self):
        self.client_dict = {}

    def start(self, address, sock):
        try:
            sock.bind(address)
            sock.listen()
            self.SERVER_STATUS = True
            with sock:
                while (self.SERVER_STATUS):
                    try:
                        self.accept_client(sock)
                    except:
                        pass
            server_shutdown(sock, self.client_dict)
        except:
            print("Could not start server")
            exit(0)

    def accept_client(self, sock):
        client, address = sock.accept()
        try:
            client.send('INFO'.encode('ascii'))
            client_info = client.recv(1024).decode('ascii')
            client_id, username = client_info.split("::::", 1)
            self.client_dict[client] = [client_id, username, address]
            msg = f'{username} joined the chat from {address}'
            broadcast(self.client_dict, msg)
        except ConnectionResetError:
            print("ConnectionResetError")
            return
        handle_thread = threading.Thread(target=self.handle, args=(client, sock,))
        handle_thread.start()

    def handle(self, client, sock):
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
                    target_client.send(message.encode('ascii'))
                else:
                    message = f"{self.client_dict[client][1]}: {recv_message}"
                    broadcast(self.client_dict, message)
            except ConnectionResetError:
                broadcast(
                    self.client_dict, f"{self.client_dict[client][1]} left the chat!")
                del self.client_dict[client]
                break
        if (not self.SERVER_STATUS):
            self.client_dict.clear()
            server_shutdown(sock, self.client_dict)
            self.SERVER_STATUS = False
            quit()
        return

    @staticmethod
    def parse_command(client, client_dict, command):
        if command == "users":
            client.send(get_str_all_val_x(client_dict, 1).encode('ascii'))
        elif command == "all":
            pass
        elif command in get_list_of_dict_idx_x(client_dict, 1):
            target_client_id = get_dict_value_x_by_value_y(
                client_dict, command, 0, 1)
            if target_client_id == None:
                client.send("Direct message target user unavailable".encode('ascii'))
            else:
                client.send(f"DIRECT::::{target_client_id}".encode('ascii'))
        elif command == "exit":
            broadcast(
                client_dict, f"{client_dict[client][1]} left the chat!")
            del client_dict[client]
            return False
        elif command == "shutdown":
            server_shutdown(client, client_dict)
            return False
        else:
            client.send(f"{command} is an invalid command".encode('ascii'))
        return True
