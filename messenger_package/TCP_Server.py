#!/usr/bin/env python3

import socketserver
import socket
import threading
import time
import re

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.server = server
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        data = str(self.request.recv(1024),'ascii')
        print(f"Server recieved: {data}")
        connect_header = 'CONNECT::::'
        disconnect_header = 'DISCONNECT::::'
        if (re.match(connect_header, data)):
            print("connecting...")
            res = re.split(connect_header, data)
            client_id = res[1]
            print(f"client_id: {client_id}")
            ThreadedTCPServer.register_client(self.server, client_id)
        if (re.match(disconnect_header, data)):
            print("disconnecting...")
            res = re.split(disconnect_header, data)
            client_id = res[1]
            print(f"client_id: {client_id}")
            ThreadedTCPServer.client_disconnect(self.server, client_id)
        cur_thread = threading.current_thread()
        cur_thread_name = cur_thread.name
        response = bytes(f"{cur_thread_name}: {data}", 'ascii')
        self.request.sendall(response)
    
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, client_address, request_handler=ThreadedTCPRequestHandler):
        self.SERVER_STATUS = True
        self.CLIENTS_UPDATE = False
        self.CLIENTS = {}
        socketserver.TCPServer.__init__(self, client_address, request_handler)
        return
    
    def get_server_thread(server):
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return server_thread
    
    @staticmethod
    def register_client(server, client_id):
        if (client_id not in server.CLIENTS):
            print(f"client_id: {client_id} not in self.clients")
            server.CLIENTS_UPDATE = True
            server.CLIENTS[client_id] = 1
        print("after add in register_client, self.clients is:")
        print(server.CLIENTS)
    
    @staticmethod
    def client_disconnect(server, client_id):
        print("before del in register_client, self.clients is:")
        print(server.CLIENTS)
        del server.CLIENTS[client_id]
        print(f"del self.clients[client_id: {client_id}]")
        server.CLIENTS_UPDATE = True