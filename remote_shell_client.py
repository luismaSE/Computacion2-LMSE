#!/usr/bin/python3
import socket, sys
import click

@click.command()
@click.option('--host')
@click.option('--port')

def client(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,int(port)))

    while True:
        msg1 = input('> ')
        s.send(msg1.encode('ascii'))
        print('ABER GASTON',msg1)
        if msg1 == 'exit':
            break
        msg2 = s.recv(1024).decode('ascii')
        print(msg2)
    s.close()
    sys.exit()
    
if __name__ == '__main__':
    client()