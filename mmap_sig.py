#!/usr/bin/python
import sys , os , mmap , argparse , signal

class App():

    def __init__(self):
        parser = argparse.ArgumentParser(description='''
El programa recibe un path_file.
Luego crea un segmento de memoria compartida y genera 2 hijos.
Leerá desde el stdin línea por línea lo que ingrese el usuario,
la almacenará en el segmento de memoria compartida y se mostrará por pantalla.
Por último, se almacenará en mayúsculas en el archivo pasado.
Para terminar el programa escribir "bye"
''')
        parser.add_argument('-f','--file',required=True,type=str,help='ruta de archivo')
        args = parser.parse_args()
        self.padre_id = os.getpid()
        
        signal.signal(signal.SIGUSR2,self.sig_USR2)
        self.mem = mmap.mmap(-1,100)
        self.file = open(args.file,'w+')

        self.h1 = os.fork() # H1
        if self.h1 == 0:
            self.f_h1()

        self.h2 = os.fork() #H2
        if self.h2 == 0:
            self.f_h2()     

        signal.signal(signal.SIGUSR1,self.sig_USR1)

        for _ in range(2):
            os.wait()   

    def f_h1(self):
        for line in sys.stdin:
            self.mem.write(line.encode())
            os.kill(os.getppid(),signal.SIGUSR1)
            if line == 'bye\n':
                os.kill(os.getppid(),signal.SIGUSR2)
                sys.exit()

    def f_h2(self):
        signal.signal(signal.SIGUSR1,self.sig_USR1)
        while True:
            signal.pause()


    def sig_USR1(self,s,f):
        if os.getpid() != self.padre_id:
            self.file.write(self.mem.readline().decode().upper())
        else:
            print(os.getpid(),'-',self.mem.readline().decode())
            os.kill(self.h2,signal.SIGUSR1)
    

    def sig_USR2(self,s,f):
        if os.getpid() != self.padre_id:
            sys.exit() 
        else:
            os.kill(self.h2,signal.SIGUSR2)


if __name__=='__main__':
    app = App()