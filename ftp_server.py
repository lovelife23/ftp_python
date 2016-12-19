import socket
import select
import sys
import time
import os

# server_address = ('127.0.0.1', 5000)
#server_address = ('192.168.43.139', 5000)
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]
print "Enter to end..."

i=0
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                i=0

            else:
                if i==0:
                    sock.send('220 Welcome!\r\n')
                    i+=1
                data = sock.recv(1024)
                data = data[:4].strip().upper()
                print data
                #sock.send('214 The following commands are recognized:\r\nCWD\r\nQUIT\r\nRETR\r\nSTOR\r\nRNTO\r\nDELE\r\nRMD\r\nMKD\r\nPWD\r\nLIST\r\nHELP\r\n')
                if data == 'QUIT':
                    sock.send('221 Goodbye.\r\n')
                    sock.close()
                    input_socket.remove(sock)
                elif data == 'TEST':
                    tes = os.getcwd()
                    #tes = os.chdir(os.path.dirname(os.getcwd()))
                    sock.send(tes)
                elif data == 'HELP':
                    sock.send('214 The following commands are recognized:\r\nCWD\r\nQUIT\r\nRETR\r\nSTOR\r\nRNTO\r\nDELE\r\nRMD\r\nMKD\r\nPWD\r\nLIST\r\nHELP\r\n')
                elif data == 'STOR':
                    sock.send('150 Opening data connection.\r\n')
                    data = sock.recv(1024)
                    size = sock.recv(1024)
                    size = int(size)
                    with open(data, 'wb') as f:
                        isi = ''
                        while 1:
                            dapet = sock.recv(1024)
                            isi += dapet
                            time.sleep(0.1)
                            if len(isi) >= size:
                                break
                        f.write(isi)
                    time.sleep(1)
                    print "DONE Upload"
                    sock.send("226 Transfer complete.\r\n")
                elif data == 'RETR':
                    sock.send('150 Opening data connection.\r\n')
                    filename = sock.recv(1024)
                    b = os.path.getsize(filename)
                    b = str(b)
                    sock.send(b)
                    b = int(b)
                    with open(filename, 'rb') as f:
                        data = ""
                        while 1:
                            baca = f.read(1024)
                            data += baca
                            time.sleep(0.1)
                            if len(data) >= b:
                                break
                        sock.send(data)
                    time.sleep(1)
                    print "DONE Download"
                    sock.send("226 Transfer complete.\r\n")

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)