#!/usr/bin/python3
import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host,port))

while True:
    msg1 = input('Enter msg: ')
    s.send(msg1.encode('ascii'))
    msg2 = s.recv(1024)
    print('Server reply:',msg2.decode('ascii'))
    if msg1 == 'exit':
        s.close()
        sys.exit()