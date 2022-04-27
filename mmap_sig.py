import sys , os , mmap , argparse , signal
'''
Escribir un programa que reciba por argumento la opción -f acompañada de un path_file.
Etapa 1:

El programa deberá crear un segmento de memoria compartida anónima, y generar dos hijos: H1 y H2

El H1 leerá desde el stdin línea por línea lo que ingrese el usuario.

Cada vez que el usuario ingrese una línea, H1 la almacenará 
en el segmento de memoria compartida, y enviará la señal USR1 al proceso padre.

El proceso padre, en el momento en que reciba la señal USR1 deberá mostrar 
por pantalla el contenido de la línea ingresada por el H1 en la memoria 
compartida, y deberá notificar al H2 usando la señal USR1.

El H2 al recibir la señal USR1 leerá la línea desde la memoria compartida 
la línea, y la almacenará en mayúsculas en el archivo pasado 
por argumento (path_file).
Etapa 2:

Cuando el usuario introduzca "bye" por terminal, el hijo H1 enviará 
la señal USR2 al padre indicando que va a terminar, y terminará.
El padre, al recibir la señal USR2 la enviará al H2, que al 
recibirla terminará también.
El padre esperará a que ambos hijos hayan terminado, 
y terminará también.'''

def f_h1(mem):
    print('soy h1')
    for line in sys.stdin:
        #print(line.upper())
        mem.write(line.encode())
        os.kill(os.getppid(),signal.SIGUSR1)
        if line == 'bye\n':
            print('me muero')
            os.kill(os.getppid(),signal.SIGUSR2)
            sys.exit()
    #sys.exit()


def f_h2():
    signal.signal(signal.SIGUSR1,sig_h2)
    print('soy h2')
    while True:
        signal.pause()


def sig_h1(s,f):
    print(mem.readline().decode())
    os.kill(h2,signal.SIGUSR1)

def sig_h2(s,f):
    file.write(mem.readline().decode().upper())

def sig_end(s,f):
    if os.getpid() != padre_id:
        sys.exit() 
    else:
        os.kill(h2,signal.SIGUSR2)


#def main():
    #parser = argparse.ArgumentParser(description=':D')
    #parser.add_argument('-f','--file',required=True,type=str,help='ruta de archivo')
    #args = parser.parse_args()


if __name__=='__main__':
    padre_id = os.getpid()
    signal.signal(signal.SIGUSR2,sig_end)
    mem = mmap.mmap(-1,100)

    file = open('/tmp/wea.txt','w+')


    print('creo h1')
    h1 = os.fork() # H1
    if h1 == 0:
        f_h1(mem)
    

    print('creo h2')
    h2 = os.fork() #H2
    if h2 == 0:
        f_h2()     

    signal.signal(signal.SIGUSR1,sig_h1)

    for hijo in range(2):
        os.wait()   