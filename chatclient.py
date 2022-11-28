import sys
import socket

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

    s = socket.socket()
    s.connect((host, port))

    #while True:

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))