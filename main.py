#!/usr/bin/env python3

import sys
import socket
from messenger_package.TCPServer import *
from messenger_package.TCPClient import *

def run(server):
    with server:
        server_thread = ThreadedTCPServer.get_server_thread(server)
        print("Server loop running in thread: ", server_thread.name)
        while(server.SERVER_STATUS):
            time.sleep(1)
            if(server.CLIENTS_UPDATE):
                print(f"self.clients_update is {server.CLIENTS_UPDATE}!")
                time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
                print(f"---------========server running at time: {time_string}========---------")
                print(server.CLIENTS)
                server.CLIENTS_UPDATE = False
    server.shutdown()
    
def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ADDR = (HOST, PORT)
    if (len(sys.argv) == 3):
        try:
            PORT = int(port)
            self.PORT = PORT
        except ValueError:
            print("Second argument not a valid port number\n==> Default port is 5050")
    if sys.argv[1] == 'server':
        print("\n-----------------Welcome to TCP Socket-Server for the Data Translator-----------------")
        print(f"Server host is: {HOST}\n at Port: {PORT}")
        print("Press [CTRL-C] close server\n")
        server = ThreadedTCPServer(ADDR, ThreadedTCPRequestHandler)
        run(server)
    elif sys.argv[1] == 'client':
        print("\n-----------------Welcome to TCP Socket-Client for the Data Translator-----------------")
        print(f"Connecting to host: {HOST}\n at port: {PORT}")
        print("Enter text and press enter to send message, 'exit' to disconnect and close client\n")
        client = TCPClient(HOST, PORT)
        client.run()
    else:
        print("Run module with 'server' or 'client' as first argument for desired function")
        print("Optional: user can select port number for server or client via second argument")
        print("For example >: python main.py server 9999")

if __name__ == '__main__':
    main()