import sys
import socket
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows

def usage():
    print("usage: chatclient.py server port", file=sys.stderr)

packet_buffer = b''

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1
    
    init_windows()

    s = socket.socket()
    s.connect((host, port))

    hello_payload = get_hello_payload(nickname)
    s.send = hello_payload.encode()

    #while True:

    s.close()

def get_hello_payload(nickname):
    hello_payload = {
    "type": "hello",
    "nick": nickname
    }

    return json.dumps(hello_payload)

def get_client_chat_payload(message):
    client_chat_payload = {
    "type": "chat",
    "message": message
    }

    return json.dumps(client_chat_payload)

if __name__ == "__main__":
    sys.exit(main(sys.argv))