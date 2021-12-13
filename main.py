#!/usr/bin/env python3

import sys
import socket


from messenger_package.Messenger_Server import *
from messenger_package.Messenger_Client import *
from messenger_package.Messenger_GUI import *
from messenger_package.Messenger_Functions import *

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    arg_len = len(sys.argv)
    if (arg_len < 2):
        print(program_info)
        return
    if (arg_len == 3):
        try:
            PORT = int(sys.argv[2])
        except ValueError:
            print(f"\n{sys.argv[2]} {invalid_port}")
            return
    ADDR = (HOST, PORT)

    print(f"\n{sys.argv[1]}, host at IP address {HOST} on port {PORT} at time {get_time()}.\n")

    if sys.argv[1] == 'server':
        try:
            server = MessengerServer()
            server.start(ADDR, SOCK)
        except: 
            print("Couldn't start server")
    elif sys.argv[1] == 'client':
        try:
            username = input("Enter username: ")
            user_id = hex(get_random_n_digit_int(9))
            client = MessengerClient()
            client.start(ADDR, SOCK, username, user_id)
        except:
            print("Couldn't start client")
    elif sys.argv[1] == 'gui':
        try:
            gui = MessengerGUI()
            WINDOW = tk.Tk()
            gui.start(ADDR, SOCK, WINDOW)
            WINDOW.mainloop()
        except:
            print("Couldn't start client")
    else:
        print(program_info)
    return

program_info = '''
            Run module with 'server' or 'client' as first argument for desired function
            Optional: Select port by passing a number between 1024 to 65535 as second argument
            Example 1) >: python main.py server
            Example 2) >: python main.py client
            Example 3) >: python main.py server 7777
            Example 4) >: python main.py client 7777
            '''

client_info ='''
            ---------------------------------------
            ----Welcome to the Messenger Client----
            ---------------------------------------\n
        Enter text and press enter to send message
        '--users' to view all clients connected to server
        '--[username]' to enable direct messaging mode to another user (ex. --willsmith)
        '--all' to enable to messaging all users (default)
        '--file [path/filename.txt] --[username]' to send file to user
            (ex. --file C:/Users/johndoe/Desktop --willsmith)
        '--save' to output message log to text file (TODO)
        '--exit' to disconnect from server and close client
            '''

server_info = '''
            ---------------------------------------
            ----Welcome to the Messenger Server----
            ---------------------------------------\n
            Press [CTRL-C] close server
            '''

invalid_port = "is not a valid port number, default port is 5050"

if __name__ == '__main__':
    main()