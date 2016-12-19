import socket
import sys
import time
import os

try:
    while True:
        #server_address = ('192.168.43.139', 5000)
        server_address = ('localhost', 5000)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client_socket.connect(server_address)
        # sys.stdout.write('>> ')

        try:
            client_socket.connect(server_address)

        except socket.error:
            print ' ! Gagal membuat soket : "Tidak bisa terhubung dengan server"'
            sys.exit()

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
            if "STOR" in msg:
                command, filename = msg.split(' ', 1)
                filename = filename.rstrip('\n')
                client_socket.send(filename)
                print filename
                b = os.path.getsize(filename)
                b = str(b)
                client_socket.send(b)
                b = int(b)
                with open(filename, 'rb') as f:
                    data = ""
                    while 1:
                        baca = f.read(1024)
                        data += baca
                        time.sleep(0.1)
                        if len(data) >= b:
                            break
                    client_socket.send(data)
                pesan = client_socket.recv(1024)
                sys.stdout.write(pesan)

except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)