import sys
import socket

def usage():
    print("usage: chatclient.py server port", file=sys.stderr)

packet_buffer = b''

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    #while True:

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))