import socket, sys, threading, multiprocessing as mp , subprocess as sp, click
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            command = self.request.recv(1024).decode("ascii")
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
            self.request.send((status+'\n'+output).encode("ascii"))
        print('Conexión terminada')
        #client.close()        


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

@click.command()
@click.option('-p',default=5000,help='Puerto del servidor')
@click.option('-c',default='t',help='(t) Para que el servidor utilice hilos o  (p) para que utilice procesos')

def server(p,c):
    #serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    #serversocket.bind((host, p))
    #serversocket.listen(5)
    socketserver.TCPServer.allow_reuse_address = True

    if c == 't':
        server = ThreadedTCPServer((host,p),MyTCPHandler)
        #threading.Thread(target=shell,args=(clientsocket,addr),daemon=True).start()
    elif c == 'p':
        server = ForkedTCPServer((host,p), MyTCPHandler)
        #mp.Process(target=shell,args=(clientsocket,addr),daemon=True).start()
    else:
        print("Parametro (c) erroneo, cerrando servidor...")
        #server.shutdown()
    
    with server:
        server.serve_forever()
        print('Iniciando server...\nEsperando a un cliente...')                                

        while True:
            #clientsocket, addr = serversocket.accept()
            print('Conexión establecida')

def shell(client,addr):
    while True:
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