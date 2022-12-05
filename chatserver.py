import sys
import socket
import random
import json
import threading
import select

# Half of the code courtesy of previous projects

def usage():
    print("usage: chatserver.py port", file=sys.stderr)

def main(argv):

    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to the chatroom")
    print("~~~~~~~~~~~~~~~~~~~~~~~")

    # Keeps track of port of clients
    client_packet_buffers = {}

    # Appends listener socket to read_sockets
    server_socket = socket.socket()
    server_socket.bind(('', port))
    server_socket.listen()
    read_sockets = {server_socket}

    while True:
        
        # Uses select to read sockets
        read, _, _ = select.select(read_sockets, {}, {})
        for s in read:
            if s == server_socket: 
                new_socket, _ = server_socket.accept()
                read_sockets.add(new_socket)

            # Regular socket, recieves data
            else:
                data = s.recv(4096) 
                if not data:
                    s.close()
                    read_sockets.remove(s)
                else:

                    chat_payload = json.loads(data.decode())

                    # Recieves hello payload if user joins
                    if chat_payload["type"] == "hello":

                        nickname = chat_payload["nick"]
                        client_packet_buffers[s] = nickname # Adds nickname to packet buffers if joining chatroom
                        server_output = "*** " + nickname + " has joined the chat"
                        print(server_output)

                    # Recieves chat payload and displays a message of a client
                    elif chat_payload["type"] == "chat":
                        nickname = client_packet_buffers[s]
                        server_output = nickname + ": " + chat_payload["message"]

                        print(server_output)
                    
                    # Sends server_output to other clients
                    for client in client_packet_buffers:
                        client.send(data)

# Following methods return json files of types chat, join, and leave
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