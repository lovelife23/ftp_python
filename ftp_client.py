import socket
import sys
import time
import os

try:
    while True:
        #server_address = ('192.168.1.47', 5000)
        server_address = ('localhost', 5000)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect(server_address)

        except socket.error:
            print '! Error\t:\tGagal membuat soket : "Tidak bisa terhubung dengan server"'
            sys.exit()

        client_socket.send(".")
        pesan = client_socket.recv(1024)
        sys.stdout.write('# Response\t:\t' + pesan)
        while True:
            msg = raw_input("> Command\t:\t")
            if 'CWD' in msg or 'QUIT' in msg or 'RETR' in msg or 'STOR' in msg or 'RNTO' in msg or 'DELE' in msg \
                    or 'RMD' in msg or 'MKD' in msg or 'PWD' in msg or 'LIST' in msg or 'HELP' in msg or "USER" in msg \
                    or "PASS" in msg or "RNFR"in msg or "RNTO" in msg or "MKD" in msg or "RMD" in msg:
                client_socket.send(msg)
                pesan = client_socket.recv(1024)
                sys.stdout.write('# Response\t:\t' + pesan)
                if '221' in pesan:
                    client_socket.close()
                    sys.exit(0)
                    break
                if 'STOR' in msg:
                    if '500 Syntax error' in pesan:
                        print 'Please reinput your command'
                    else:
                        command, filename = msg.split(' ', 1)
                        filename = filename.rstrip('\n')
                        client_socket.send(filename)
                        print '+ Status\t:\tUploading ' + filename
                        b = os.path.getsize(filename)
                        b = str(b)
                        client_socket.send(b)
                        b = int(b)
                        with open(filename, 'rb') as f:
                            data = ""
                            while 1:
                                baca = f.read(1024)
                                data += baca
                                if len(data) >= b:
                                    break
                            client_socket.send(data)
                        #time.sleep(1)
                        pesan = client_socket.recv(1024)
                        sys.stdout.write('# Response\t:\t' + pesan)
                if 'RETR' in msg:
                    if '500 Syntax error' in pesan:
                        print 'Please reinput your command'
                    else:
                        flag = ''
                        command, filename = msg.split(' ', 1)
                        filename = filename.rstrip('\n')
                        client_socket.send(filename)
                        print '+ Status\t:\tDownloading ' + filename
                        size = client_socket.recv(1024)
                        size = int(size)
                        with open(filename, 'wb') as f:
                            isi = ''
                            while 1:
                                dapet = client_socket.recv(1024)
                                if '226 ' in dapet:
                                    flag += dapet.split('226 ')[1]
                                    isi += dapet.split('226 ')[0]
                                else:
                                    isi += dapet
                                if len(isi) >= size:
                                    break
                            f.write(isi)
                        #time.sleep(1)
                        if flag:
                            print '# Response\t:\t226 Transfer complete.\r\n'
                        else:
                            pesan = client_socket.recv(1024)
                            sys.stdout.write('# Response\t:\t' + pesan)

                if 'DELE' in msg:
                    command, filename = msg.split(' ', 1)
                    filename = filename.rstrip('\n')
                    client_socket.send(filename)
                    pesan = client_socket.recv(1024)
                    sys.stdout.write('# Response\t:\t' + pesan)
            else:
                print '! Error\t\t:\tWrong Command, Try HELP to view all available commands'

except KeyboardInterrupt:
    client_socket.close()
sys.exit(0)
