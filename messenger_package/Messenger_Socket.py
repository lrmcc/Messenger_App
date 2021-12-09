import socket


def get_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Could not create socket")
        quit()
    return sock


def server_shutdown(srvr, client_dict):
    broadcast_message(client_dict, "server_shutdown")
    broadcast_message(client_dict, "REFUSE")
    srvr.shutdown()
    srvr.close()


def direct_message(sock, message):
    try:
        sock.send(message.encode('ascii'))
    except ConnectionResetError:
        print("direct_message ConnectionResetError")
        pass


def broadcast_message(client_dict, message):
    # takes in a dictionary where each key is a socket connection
    for key in client_dict:
        with get_socket() as sock:
            try:
                key.send(message.encode('ascii'))
            except ConnectionResetError:
                print("broadcast_message ConnectionResetError")
                continue
