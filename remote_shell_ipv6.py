import sys, socket, threading, socketserver, subprocess as sp, click
from ordered_set import T


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

class ThreadedTCPServer_ipv6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass

class ForkedTCPServer_ipv6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass





def s_ipv4(host,p,c):
    print("instanciado servidor para IPV4")
    if c == 't':
        server = ThreadedTCPServer((host,p),MyTCPHandler)
    elif c == 'p':
        server = ForkedTCPServer((host,p), MyTCPHandler)
    else:
        print("Parametro (c) erroneo, cerrando servidor...")
        sys.exit(0)
    with server:
        print('(IPV4) - Iniciando server...\nEsperando a un cliente...')                                
        server.serve_forever()



def s_ipv6(host,p,c):
    print("instanciado servidor para IPV6")
    if c == 't':
        server_ipv6 = ThreadedTCPServer_ipv6((host,p),MyTCPHandler)
    elif c == 'p':
        server_ipv6 = ForkedTCPServer_ipv6((host,p), MyTCPHandler)
    else:
        print("Parametro (c) erroneo, cerrando servidor...")
        sys.exit(0)
    with server_ipv6:
        print('(IPV6) - Iniciando server...\nEsperando a un cliente...')                                
        server_ipv6.serve_forever()








@click.command()
@click.option('-p',default=5000,help='Puerto del servidor')
@click.option('-c',default='t',help='(t) Para que el servidor utilice hilos o  (p) para que utilice procesos')

def server(p,c):
    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost",5000,socket.AF_INET,1)[0])
    direcciones.append(socket.getaddrinfo("localhost",5000,socket.AF_INET6,1)[0])

    socketserver.TCPServer.allow_reuse_address = True

    threading.Thread(target=s_ipv4,args=(direcciones[0][4][0],p,c),daemon=False).start()
    threading.Thread(target=s_ipv6,args=(direcciones[1][4][0],p+1,c),daemon=False).start()

if __name__ == "__main__":
    server()