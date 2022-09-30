#!/usr/bin/python3
import socket, sys
import click

@click.command()
@click.option('-h')
@click.option('-p')

def client(h,p):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((h,int(p)))

    while True:
        msg1 = input('> ')
        s.send(msg1.encode('ascii'))
        if msg1 == 'exit':
            break
        msg2 = s.recv(1024).decode('ascii')
        print(msg2)
    s.close()
    sys.exit()
    
if __name__ == '__main__':
    client()