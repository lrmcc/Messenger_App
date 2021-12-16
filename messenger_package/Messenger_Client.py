import threading

from messenger_package.Messenger_Socket import *
from messenger_package.Messenger_Functions import *


class MessengerClient():
    def __init__(self):
        print("client init!")
        self.message_header = ""
        self.last_message_sent = ""

    def start(self, addr, sock, username, user_id):
        print()
        try:
            print("client start!")
            
            user_thread = threading.Thread(
                target=self.get_user_input, args=(sock,))
            print("user_thread")
            
            recieve_thread = threading.Thread(
                target=self.receive_from_server, args=(sock,))
            print("recieve_thread")
            
            sock.connect(addr)
            print("sock.connect(addr)")
            
            connect_message = sock.recv(1024).decode('ascii')
            if connect_message == 'INFO':
                print("if connect_message == INFO:")
                info = f"{user_id}::::{username}"
                sock.send(info.encode('ascii'))
                recieve_thread.start()
                user_thread.start()
            else:
                print("Server has not accepted connection")
        except:
            print("Messenger_Client.py: Could not start messenger client")
            sock.close()
            quit()

    def get_user_input(self, client):
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

    def receive_from_server(self, client):
        while True:
            try:
                recv_message = client.recv(1024).decode('ascii')
                print(recv_message)
                response = MessengerClient.parse_recieve(
                    client, recv_message, self.last_message_sent)
                if recv_message != response:
                    self.message_header = response
            except:
                print("An exception occurred during message recieve")
                client.close()
                quit()

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
