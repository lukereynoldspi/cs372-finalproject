import sys
import socket
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows

def usage():
    print("usage: chatclient.py server port", file=sys.stderr)

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

    sending_thread = threading.Thread(target=send_client_input, args=(s, nickname))
    recieving_thread = threading.Thread(target=recieve_server_output, args=(s))

    hello_payload = get_hello_payload(nickname)
    s.send(hello_payload.encode())

    
def send_client_input(port, nickname):
    while True:
        message = read_command(nickname + "> ")

        for letter in message:
            if letter == "/":
                if message[letter + 1] == "q":
                    port.close()
        else:
            client_chat_payload = get_client_chat_payload(message)
            port.send(client_chat_payload.encode())

def recieve_server_output(port):
    pass


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