import sys
import socket
import random

def usage():
    print("usage: chatserver.py port", file=sys.stderr)

def main(argv):

    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    s = socket.socket()
    s.bind(('', port))
    s.listen()

    while True:
        print("-----------------------")
        print("Welcome to the chatroom")
        print("-----------------------")

        new_s, connection_info = s.accept()

        print(f"Got connection from {connection_info}")

        new_s.close()
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))