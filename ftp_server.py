import socket
import select
import sys
import time
import os
import os.path
from datetime import datetime

# server_address = ('127.0.0.1', 5000)
# server_address = ('192.168.43.139', 5000)
server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

user = "admin"
pwd = "admin"
loginflag = 0;
renameflag = 0;
input_socket = [server_socket]
print '>> FTP Server - Progjar C 2016\r\n'
UN = '(not logged in)'
PW = ''
prevname = ''
i = 0
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                time = datetime.now()
                print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> Connected, sending welcome message...'
                i = 0
            else:
                if i == 0:
                    print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> 220-FTP Server Progjar C 2016'
                    sock.send('220 Welcome! - FTP Server Progjar C 2016\r\n')
                    i += 1
                data = sock.recv(1024)
                login = data
                data = data[:4].strip().upper()
                if not data == '.':
                    if loginflag == 0:
                        if data == 'QUIT':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> disconnected'
                            sock.send('221 Goodbye.\r\n')
                            sock.close()
                            input_socket.remove(sock)
                        elif data == 'USER':
                            UN = login.split(" ")[1]
                            sock.send("enter your password\r\n")
                        elif data == 'PASS':
                            PW = login.split(" ")[1]
                            if PW == pwd and UN == user:
                                sock.send("230 User logged in, proceed.\r\n")
                                loginflag = 1;
                            else:
                                UN = ''
                                PW = ''
                                sock.send("530 Login or password incorrect!\r\n");
                                loginflag = 0;
                        elif data == 'HELP':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> 214 Have a nice day.'
                            sock.send(
                                '214 The following commands are recognized:\r\nUSER\tPASS\tCWD\r\nQUIT\tRETR\tSTOR'
                                '\r\nRNTO\tDELE\tRMD\r\nMKD\t\tPWD\t\tLIST\r\nHELP\r\n')
                        else:
                            sock.send("Please Login using USER and PASS command.\r\n")
                    elif loginflag != 0:
                        print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '>', data
                        if data == 'QUIT':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> disconnected'
                            sock.send('221 Goodbye.\r\n')
                            sock.close()
                            input_socket.remove(sock)
                        elif data == 'PWD':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> PWD'
                            loc = os.getcwd()
                            # tes = os.chdir(os.path.dirname(os.getcwd()))
                            sock.send(loc + '\n')
                        elif data == 'CWD':
                            dirname = login.split(" ")[1]
                            loc = os.getcwd()
                            isi = os.listdir(loc)
                            if dirname == "..":
                                os.chdir(dirname)
                                loc = os.getcwd()
                                sock.send('250 Working directory changed.\r\n')
                                # tes = os.chdir(os.path.dirname(os.getcwd()))
                                sock.send(loc + '\n')
                                # elif isi:
                                #   response_data = ""
                                #   flag = 0
                                #  for file in isi:
                                #     if file == dirname:
                                #       loc = os.getcwd()
                                #       # tes = os.chdir(os.path.dirname(os.getcwd()))
                                #      sock.send(loc + '\n')
                                #     flag = 1
                                # if flag == 0:
                                #   sock.send("no such name in directory\n")
                                # else:
                                #   sock.send("no files in directory\n")
                            else:
                                if os.path.isdir(dirname):
                                    os.chdir(dirname)
                                    sock.send('250 Working directory changed.\r\n')
                                else:
                                    sock.send("directory not found.\r\n")

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
                        elif data == 'RNFR':
                            prevname = login.split(" ")[1]
                            loc = os.getcwd()
                            loc = loc + "\\" + prevname
                            #print loc
                            if os.path.exists(loc):
                                if os.path.isfile(loc):
                                    prevname = prevname
                                    sock.send("350 Ready.\r\n")
                                    renameflag = 1
                                else:
                                    prevname = ''
                                    renameflag = 0
                                    sock.send("the requested item is not a valid file.\r\n")
                            else:
                                prevname = ''
                                renameflag = 0
                                sock.send("File not found.\r\n")
                        elif data == 'RNTO':
                            newname = login.split(" ")[1]
                            if renameflag is not 0:
                                os.rename(prevname, newname)
                                prevname = ''
                                newname = ''
                                sock.send("250 File renamed.\r\n")
                            else:
                                sock.send("do a valid RNFR command first\r\n")

                        elif data=='MKD':
                            dir=login.split(" ")[1]
                            loc=os.getcwd()
                            loc = loc + "\\" + dir
                            if not os.path.isdir(loc):
                                os.mkdir(loc)
                                sock.send("directory created\r\n")
                            else:
                                sock.send("directory name is already been used\r\n")

                        elif data=='RMD':
                            dir = login.split(" ")[1]
                            loc = os.getcwd()
                            loc = loc + "\\" + dir
                            if os.path.isdir(loc):
                                os.rmdir(loc)
                                sock.send ("directory deleted\r\n")
                            else:
                                sock.send("directory is not exist\r\n")


                        elif data == 'HELP':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> 214 Have a nice day.'
                            sock.send(
                                '214 The following commands are recognized:\r\nUSER\tPASS\tCWD\r\nQUIT\tRETR\tSTOR'
                                '\r\nRNTO\tDELE\tRMD\r\nMKD\t\tPWD\t\tLIST\r\nHELP\r\n')
                        elif data == 'STOR':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address,\
                                '> 150 Opening data connection.'
                            sock.send('150 Opening data connection.\r\n')
                            data = sock.recv(1024)
                            size = sock.recv(1024)
                            size = int(size)
                            with open(data, 'wb') as f:
                                isi = ''
                                while 1:
                                    dapet = sock.recv(1024)
                                    isi += dapet
                                    #time.sleep(0.1)
                                    if len(isi) >= size:
                                        break
                                f.write(isi)
                            #time.sleep(1)
                            sock.send("226 Transfer complete.\r\n")
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> 226 Transfer complete.'
                        elif data == 'RETR':
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address,\
                                '> 150 Opening data connection.'
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
                                sock.send("226 Transfer complete.\r\n")
                            #time.sleep(1)
                            print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address, '> Download Finished.'





                        elif data == 'DELE':
                            sock.send('Deleting Files...\r\n')
                            filename = sock.recv(1024)
                            allow_delete = True
                            if allow_delete:
                                os.remove(filename)
                                print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address,\
                                    '> 250 File deleted successfully.'
                                sock.send('250 File deleted successfully\r\n')
                                allow_delete = False
                            else:
                                print time.strftime('%Y/%m/%d %H:%M:%S'), UN, client_address,\
                                    '> 450 Not Allowed.'
                                self.send('450 Not Allowed.\r\n')

except KeyboardInterrupt:
    server_socket.close()
sys.exit(0)
