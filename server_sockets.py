from os import getgid
import socket, sys, os
import threading, time


def connect(client,addr):
    while True:
        inp = client.recv(1024)
        msg = inp.decode("ascii")
        print("Recibido: "+msg)
        if msg != 'exit':
            outp = msg.upper()
            client.send(outp.encode('ascii'))
        else:
            client.send('Desconectado...'.encode('ascii'))
            client.close()
            print('Conexión terminada con el Ciente:',addr)
            break

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = ""
    port = int(sys.argv[1])
    serversocket.bind((host, port))                                  
    print('Iniciando server...\nEsperando a un cliente...')
    serversocket.listen(5)
    while True:
        clientsocket, addr = serversocket.accept()
        print('Conexión establecida, Cliente:',addr)
        threading.Thread(target=connect,args=(clientsocket,addr),daemon=True).start()
        input('seguir?')


if __name__ == '__main__':
    main()