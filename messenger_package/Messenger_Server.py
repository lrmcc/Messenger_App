#!/usr/bin/env python3

import socketserver
import socket
import threading
import time
import re

class MessengerTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.server = server
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        data = str(self.request.recv(1024),'ascii')
        self.parse_data(data)
        
        cur_thread = threading.current_thread()
        cur_thread_name = cur_thread.name
        response = bytes(f"{cur_thread_name}: {data}", 'ascii')
        self.request.sendall(response)

    def parse_data(self, data):
        message_header, message_payload = re.split("::::", data)
        print(f"message_header: {message_header} message_payload: {message_payload}")
        if (message_header == 'CONNECT'):
            print("connecting...")
            print(f"client_id: {message_payload}")
            MessengerTCPServer.register_client(self.server, message_payload)
        if (message_header == 'DISCONNECT'):
            print("disconnecting...")
            print(f"client_id: {message_payload}")
            MessengerTCPServer.disconnect_client(self.server, message_payload)
    
class MessengerTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, client_address, request_handler=MessengerTCPRequestHandler):
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
            server.CLIENTS_UPDATE = True
            server.CLIENTS[client_id] = 1
        print(server.CLIENTS)
    
    @staticmethod
    def disconnect_client(server, client_id):
        print(server.CLIENTS)
        del server.CLIENTS[client_id]
        server.CLIENTS_UPDATE = True