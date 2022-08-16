from os import getgid
import socket, sys, os
import threading


def connect(client):
    print('soy un hilo')
    while True:
        inp = client.recv(1024)

        msg = inp.decode("ascii")
        print("Recibido: "+msg)
        if msg != 'exit':
            outp = msg.upper()
            client.send(outp.encode('ascii'))
        else:
            os._exit(0)

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = ""
    port = int(sys.argv[1])
    serversocket.bind((host, port))                                  
    print('Iniciando server...')
    serversocket.listen(5)
    while True:
        print('soy el padre',os.getpid())
        clientsocket, addr = serversocket.accept()
        print("Address: %s " % str(addr))
        threading.Thread(target=connect,args=(clientsocket,),daemon=True).start()
        print('cree un hilo')

if __name__ == '__main__':
    main()