import socket
import select
import sys
import time
import os

# server_address = ('127.0.0.1', 5000)
# server_address = ('192.168.43.139', 5000)
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
print 'FTP Server - Progjar C 2016\r\n'
UN = 'Not Logged In'
i = 0
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                print UN, client_address, '> Connected, sending welcome message...'
                i = 0
            else:
                if i == 0:
                    print UN, client_address, '> 220-FTP Server Progjar C 2016'
                    sock.send('220 Welcome!\r\n')
                    i += 1
                data = sock.recv(1024)
                data = data[:4].strip().upper()
                if not data == '.':
                    print UN, client_address, '>', data
                if data == 'QUIT':
                    print UN, client_address, '> disconnected'
                    sock.send('221 Goodbye.\r\n')
                    sock.close()
                    input_socket.remove(sock)

                elif data == 'PWD':
                    print UN, client_address, '> PWD'
                    loc = os.getcwd()
                    # tes = os.chdir(os.path.dirname(os.getcwd()))
                    sock.send(loc + '\n')
                elif data == 'CWD':
                    sock.send('250 Working directory changed.\r\n')
                    dirname = sock.recv(1024)
                    loc = os.getcwd()
                    isi = os.listdir(loc)
                    if dirname == "..":
                        os.chdir(dirname)
                        loc = os.getcwd()
                        # tes = os.chdir(os.path.dirname(os.getcwd()))
                        sock.send(loc + '\n')
                    elif isi:
                        response_data = ""
                        flag = 0
                        for file in isi:
                            if file == dirname:
                                os.chdir(loc + "/" + dirname)
                                loc = os.getcwd()
                                # tes = os.chdir(os.path.dirname(os.getcwd()))
                                sock.send(loc + '\n')
                                flag = 1
                        if flag == 0:
                            sock.send("no such name in directory\n")
                    else:
                        sock.send("no files in directory\n")
                elif data == 'LIST':
                    path = os.getcwd()
                    response_data = ""
                    isi = os.listdir(path)
                    if isi:
                        for file in isi:
                            response_data = response_data + file + "\n"
                        sock.send(response_data)
                    else:
                        sock.send("no files in directory\n")

                elif data == 'HELP':
                    print UN, client_address, '> 214 Have a nice day.'
                    sock.send(
                        '214 The following commands are recognized:\r\nCWD\t\tQUIT\tRETR\r\nSTOR\tRNTO\tDELE\r\nRMD'
                        '\t\tMKD\t\tPWD\r\nLIST\tHELP\r\n')
                elif data == 'STOR':
                    print UN, client_address, '> 150 Opening data connection.'
                    sock.send('150 Opening data connection.\r\n')
                    data = sock.recv(1024)
                    size = sock.recv(1024)
                    size = int(size)
                    with open(data, 'wb') as f:
                        isi = ''
                        while 1:
                            dapet = sock.recv(1024)
                            isi += dapet
                            # time.sleep(0.1)
                            if len(isi) >= size:
                                break
                        f.write(isi)
                    time.sleep(1)
                    print UN, client_address, '> 226 Transfer complete.'
                    sock.send("226 Transfer complete.\r\n")
                elif data == 'RETR':
                    print UN, client_address, '> 150 Opening data connection.'
                    sock.send('150 Opening data connection.\r\n')
                    filename = sock.recv(1024)
                    filesize = os.path.getsize(filename)
                    filesize = str(filesize)
                    sock.send(filesize)
                    filesize = int(filesize)
                    with open(filename, 'rb') as f:
                        data = ""
                        while 1:
                            baca = f.read(1024)
                            data += baca
                            if len(data) >= filesize:
                                break
                        sock.send(data)
                    time.sleep(1)
                    print UN, client_address, '> Download Finished.'
                    sock.send("226 Transfer complete.\r\n")
                elif data == 'DELE':
                    sock.send('Deleting Files....\r\n')
                    filename = sock.recv(1024)
                    allow_delete = True
                    if allow_delete:
                        os.remove(filename)
                        print UN, client_address, '> 250 File deleted successfully.'
                        sock.send('250 File deleted successfully\r\n')
                        allow_delete = False
                    else:
                        print UN, client_address, '> 450 Not Allowed.'
                        self.send('450 Not Allowed.\r\n')

except KeyboardInterrupt:
    server_socket.close()
sys.exit(0)
