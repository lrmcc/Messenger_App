import socket

def server_shutdown(srvr, client_dict):
    broadcast(client_dict, "server_shutdown")
    broadcast(client_dict, "REFUSE")
    srvr.shutdown()
    srvr.close()

def broadcast(client_dict, message):
    # takes in a dictionary where each key is a socket connection
    for key in client_dict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                key.send(message.encode('ascii'))
            except ConnectionResetError:
                print("broadcast_message ConnectionResetError")
