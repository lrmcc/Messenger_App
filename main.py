#!/usr/bin/env python3

import getpass
import socket
import sys
import time

from messenger_package.Messenger_Client import *
from messenger_package.Messenger_Server import *


def run(server):
    with server:
        server_thread = MessengerTCPServer.get_server_thread(server)
        print("Server loop running in thread: ", server_thread.name)
        while(server.SERVER_STATUS):
            pass
    server.shutdown()
    
def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ADDR = (HOST, PORT)
    if (len(sys.argv) == 3):
        try:
            PORT = int(sys.argv[2])
        except ValueError:
            print(port_message)
    if sys.argv[1] == 'server':
        print(server_message)
        print(f"Server host is: {HOST}\n at Port: {PORT}")
        server = MessengerTCPServer(ADDR, MessengerTCPRequestHandler)
        run(server)
    elif sys.argv[1] == 'client':
        USER = getpass.getuser()
        print(f"USER: {USER}")
        print(client_message)
        print(f"Client connecting to host: {HOST}\n at port: {PORT}")
        client = MessengerClient(HOST, PORT, USER)
        client.run()
    else:
        print(messenger_message)

client_message = '''
                    \n
                    -------- Welcome to the Messenger Client --------
                    Enter text and press enter to send message
                    '--clients' to see all connected users
                    '--exit' to disconnect and close client
                    \n
                    '''
server_message = '''
                    \n
                    -------- Welcome to the Messenger Server --------
                    Press [CTRL-C] close server
                    \n    
                    '''
messenger_message = '''
                    \n
                    Run module with 'server' or 'client' as first argument for desired function
                    Optional: user can select port number for server or client via second argument
                    For example >: python main.py server 9999
                    \n
                    '''
port_message = "Second argument not a valid port number\n==> Default port is 5050"

if __name__ == '__main__':
    main()
