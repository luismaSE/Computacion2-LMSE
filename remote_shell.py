from ast import Pass
import sys, socketserver, subprocess as sp, click


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('Coneccion establecida, con el cliente:',self.client_address)
        while True:
            command = self.request.recv(1024).decode("ascii")
            if command != 'exit':
                try:
                    p = sp.Popen(str(command).split(),stdout=sp.PIPE,stderr=sp.PIPE)   
                    if p.communicate()[1] != b'':
                        status = 'ERROR'
                        output = (p.communicate()[1]).decode('ascii')
                    else:
                        status = 'OK'
                        output = (p.communicate()[0]).decode('ascii')
                except FileNotFoundError:
                    status,output = 'ERROR',('FileNotFoundError: [Errno 2] No such file or directory:'+command)
                except:
                    status,output = 'ERROR','Comando erroneo'
            else:
                status,output = 'OK','bye'
                break
            self.request.send((status+'\n'+output).encode("ascii"))
        print('Conexión terminada, con el cliente:',self.client_address)
             



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


@click.command()
@click.option('-p',default=5000,help='Puerto del servidor')
@click.option('-c',default='t',help='(t) Para que el servidor utilice hilos o  (p) para que utilice procesos')

def server(p,c):
    host = "localhost"
    socketserver.TCPServer.allow_reuse_address = True

    if c == 't':
        server = ThreadedTCPServer((host,p),MyTCPHandler)
    elif c == 'p':
        server = ForkedTCPServer((host,p), MyTCPHandler)
    else:
        print("Parametro (c) erroneo, cerrando servidor...")
        sys.exit(0)
    
    with server:
        print('Iniciando server...\nEsperando a un cliente...')                                
        server.serve_forever()


if __name__ == "__main__":
    server()