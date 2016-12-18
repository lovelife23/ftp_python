import socket
import sys
import time
import os

#server_address = ('172.20.10.2', 5000)
server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

#sys.stdout.write('>> ')

try:
        client_socket.send(".")
        pesan = client_socket.recv(1024)
        sys.stdout.write(pesan)
        while True:
            msg = raw_input(">> ")
            #client_socket.send(".")
            client_socket.send(msg)
            pesan = client_socket.recv(1024)
            sys.stdout.write(pesan)
            if "221" in pesan:
                # sys.stdout.write(pesan)
                client_socket.close()
                sys.exit(0)
                break

except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)