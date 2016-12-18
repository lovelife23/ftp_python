import socket
import select
import sys

# server_address = ('127.0.0.1', 5000)
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

            else:
                if (i==0):
                    sock.send('220 Welcome!\r\n')
                    i+=1
                data = sock.recv(1024)
                data = data[:4].strip().upper()
                print data
                #sock.send('214 The following commands are recognized:\r\nCWD\r\nQUIT\r\nRETR\r\nSTOR\r\nRNTO\r\nDELE\r\nRMD\r\nMKD\r\nPWD\r\nLIST\r\nHELP\r\n')
                if (data == 'QUIT'):
                    sock.send('221 Goodbye.\r\n')
                    sock.close()
                    input_socket.remove(sock)
                elif (data == 'HELP'):
                    sock.send('214 The following commands are recognized:\r\nCWD\r\nQUIT\r\nRETR\r\nSTOR\r\nRNTO\r\nDELE\r\nRMD\r\nMKD\r\nPWD\r\nLIST\r\nHELP\r\n')

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)