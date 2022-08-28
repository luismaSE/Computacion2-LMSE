from email.policy import default
import socket, sys, threading
import click
import subprocess as sp

@click.command()
@click.option('--port',default=5000,help='Puerto del servidor')
#@click.option('--c',help='(t) Para que el servidor utilice hilos')
#@click.option('-c p',help='Para que el servidor utilice procesos')

def server(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    #port = int(sys.argv[1])
    serversocket.bind((host, port))
    print('Iniciando server...\nEsperando a un cliente...')                                
    serversocket.listen(5)

    while True:
        clientsocket, addr = serversocket.accept()
        print('Conexión establecida, Cliente:',addr)
        threading.Thread(target=shell,args=(clientsocket,addr),daemon=True).start()


def shell(client,addr):
    while True:
        #client.send("Ingrese el comando:\n> ".encode("ascii"))
        command = client.recv(1024).decode("ascii")
        if command != 'exit':
            p = sp.Popen(str(command).split(),stdout=sp.PIPE,stderr=sp.PIPE)
            if p.communicate()[1] != b'':
                status = 'ERROR'
                output = (p.communicate()[1]).decode('ascii')
            else:
                status = 'OK'
                output = (p.communicate()[0]).decode('ascii')
        else:
            status,output = 'OK','bye'
            break
        client.send((status+'\n'+output).encode("ascii"))
    print('Conexión terminada con el Ciente:',addr)
    client.close()



if __name__ == "__main__":
    server()