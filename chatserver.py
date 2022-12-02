import sys
import socket
import random
import json
import threading

def usage():
    print("usage: chatserver.py port", file=sys.stderr)

def main(argv):

    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    print("-----------------------")
    print("Welcome to the chatroom")
    print("-----------------------")

    # Makes dict and set for buffers/sockets
    client_packet_buffers = {}
    read_sockets = []

    # Appends listener socket to read_sockets
    s = socket.socket()
    s.bind(('', port))
    s.listen()
    read_sockets.append(s)

    while True:


        new_s, connection_info = s.accept()

        print(f"Got connection from {connection_info}")

        new_s.close()

def get_server_chat_payload(nickname, message):
    server_chat_payload = {
    "type": "chat",
    "nick": nickname,
    "message": message
    }

    return json.dumps(server_chat_payload)

def get_join_payload(joiner_nickname):
    join_payload = {
    "type": "join",
    "nick": joiner_nickname
    }

    return json.dumps(join_payload)

def get_leave_payload(leaver_nickname):
    leave_payload = {
    "type": "leave",
    "nick": leaver_nickname
    }

    return json.dumps(leave_payload)
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))