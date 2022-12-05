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
    hello_payload = get_hello_payload(nickname)
    s.send(hello_payload.encode())

    sending_thread = threading.Thread(target=send_client_input, args=(s, nickname))
    recieving_thread = threading.Thread(target=recieve_server_output, args=(s,), daemon=True)

    threads = [sending_thread, recieving_thread]

    for thread in threads:
        thread.start()

    threads[0].join()

    end_windows()
    
def send_client_input(port, nickname):
    while True:
        message = read_command(nickname + "> ")

        for letter in range(0, len(message)):
            if message[letter] == "/":
                if message[letter + 1] == "q":
                    port.close()
                    
        else:
            client_chat_payload = get_client_chat_payload(message)
            port.send(client_chat_payload.encode())

def recieve_server_output(port):
    while True:
        chat_payload = json.loads(port.recv(4096).decode())

        nickname = chat_payload["nick"]
        message = chat_payload["message"]

        if chat_payload["type"] == "chat":
            server_output = nickname + ": " + message
        elif chat_payload["type"] == "join":
            server_output = "*** " + nickname + " has joined the chat"
        elif chat_payload["type"] == "leave":
            server_output = "*** " + nickname + " has left the chat"
            
        print_message(server_output)

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