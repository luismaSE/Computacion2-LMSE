import sys, socket, concurrent.futures , subprocess as sp, click

def handle(clientsocket):
    sock , addr = clientsocket
    print('Coneccion establecida, con el cliente:', addr)
    while True:
        command = sock.recv(1024).decode("ascii")
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
        sock.send((status+'\n'+output).encode("ascii"))
    print('Conexión terminada, con el cliente:',addr)      

@click.command()
@click.option('-p',default=5000,help='Puerto del servidor')
@click.option('-c',default='t',help='(t) Para que el servidor utilice hilos o  (p) para que utilice procesos')

def server(p,c):
    host = "localhost"
    if c == 't':
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    elif c == 'p':
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    else:
        print("Parametro (c) erroneo, cerrando servidor...")
        sys.exit(0)
    
    print('Iniciando server...\nEsperando a un cliente...')                               
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as server:
        server.bind((host,p))
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.listen(5)
        while True:
            clientsocket = server.accept()
            executor.submit(handle,clientsocket)

if __name__ == "__main__":
    server()