import asyncio, argparse , subprocess as sp


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ho",'--host', type=str, default="localhost" , required=True, help="Dirección IP o nombre del servidor al que conectarse")
    parser.add_argument("-p",'--port', type=int, default=5000 , help="Puerto del servidor")
    return parser.parse_args()


async def handle(reader, writer):
    while True:
        command = await reader.read(100)
        command = command.decode()
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

        writer.write((status+'\n'+output).encode())
        await writer.drain()
    writer.close()
             


# Al usar Click tira el siguiente error: 'sys:1: RuntimeWarning: coroutine 'main' was never awaited'
# Asi que decidi usar argparse

# @click.command()
# @click.option('-h',default="localhost",help='Dirección IP o nombre del servidor al que conectarse')
# @click.option('-p',default=5000,help='Puerto del servidor')


async def main():
    args = argumentos()
    server = await asyncio.start_server(handle,args.host,args.port)

    async with server:
        print('Iniciando server...\nEsperando a un cliente...')  
        # print(f"Tareas:\n{asyncio.all_tasks()}")
        await server.serve_forever()



if __name__ == '__main__':
    asyncio.run(main())