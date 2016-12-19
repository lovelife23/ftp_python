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
            if "CWD" in msg or "QUIT" in msg or "RETR" in msg or "STOR" in msg or "RNTO" in msg or "DELE" in msg or "RMD" in msg or "MKD" in msg or "PWD" in msg or "LIST" in msg or "HELP" in msg:
                #client_socket.send(".")
                client_socket.send(msg)
                pesan = client_socket.recv(1024)
                sys.stdout.write(pesan)
                if "221" in pesan:
                    # sys.stdout.write(pesan)
                    client_socket.close()
                    sys.exit(0)
                    break
                if "CWD" in msg:
                    command, filename = msg.split(' ', 1)
                    filename = filename.rstrip('\n')
                    client_socket.send(filename)
                    pesan = client_socket.recv(1024)
                    sys.stdout.write(pesan)
                if "STOR" in msg:
                    command, filename = msg.split(' ', 1)
                    filename = filename.rstrip('\n')
                    client_socket.send(filename)
                    print 'Uploading ' + filename
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
                    time.sleep(1)
                    pesan = client_socket.recv(1024)
                    sys.stdout.write(pesan)
                if "RETR" in msg:
                    command, filename = msg.split(' ', 1)
                    filename = filename.rstrip('\n')
                    client_socket.send(filename)
                    print 'Downloading ' + filename
                    size = client_socket.recv(1024)
                    size = int(size)
                    with open(filename, 'wb') as f:
                        isi = ''
                        while 1:
                            dapet = client_socket.recv(1024)
                            isi += dapet
                            time.sleep(0.1)
                            if len(isi) >= size:
                                break
                        f.write(isi)
                    time.sleep(1)
                    pesan = client_socket.recv(1024)
                    #pesan = client_socket.recv(1024)
                    sys.stdout.write(pesan)
                if "DELE" in msg:
                    command, filename = msg.split(' ', 1)
                    filename = filename.rstrip('\n')
                    client_socket.send(filename)
                    pesan = client_socket.recv(1024)
                    sys.stdout.write(pesan)
            else:
                pesan = client_socket.recv(1024)
                print "Wrong Command, Try HELP to view all available commands"

except KeyboardInterrupt:
        client_socket.close()
sys.exit(0)
