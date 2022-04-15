#!/usr/bin/python
'''
./escritores.py -n 3 -r 4 -f /tmp/letras.txt

ABCACBABCBAC

./escritores.py -n 3 -r 5 -f /tmp/letras.txt -v

Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401708 escribiendo letra 'B'

Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

-n <N>
-r <R>
-h
-f <ruta_archivo>
-v

El programa deberá abrir (crear si no existe) un archivo de texto cuyo path ha sido pasado por argumento con -f.

El programa debe generar <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto 
(el primer proceso con la "A", el segundo con la "B", etc). 
Cada proceso almacenará en el archivo su letra <R> veces con un delay de un segundo entre escritura y escritura 
(realizar flush() luego de cada escritura).

El proceso padre debe esperar a que los hijos terminen, 
luego de lo cual deberá leer el contenido del archivo y mostrarlo por pantalla.

La opción -h mostrará ayuda. La opción -v activará el modo verboso, 
en el que se mostrará antes de escribir cada letra en el archivo: Proceso <PID> escribiendo letra 'X'.
'''

import argparse
import os
import sys
import subprocess as sp
import time


def main():
    parser = argparse.ArgumentParser(description=
    '''El programa abre o crea un archivo de texto cuyo path ha sido pasado por argumento con -f.
    Luego, genera <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto.
    Cada proceso almacenará en el archivo su letra <R> veces con un delay.
    ''')
    parser.add_argument('-n','--number',type=int,required=True,help='numero de procesos hijos que se van a crear')
    parser.add_argument('-r', '--repeat',type=int,required=True,help='Cantidad de veces que cada proceso hijo guardará su letra en el archivo')
    parser.add_argument('-f','--file',type=str,required=True,help='Ruta del archivo donde trabajará el programa')
    parser.add_argument('-v', '--verb',action='store_true',help='activa el modo verboso')
    args = parser.parse_args()
    #open(args.file,'w')  # sobreescribe el contenido anterior del archivo, para que el output sea solo el de la ultima vez que se ejecutó
    char = 0
    with open(args.file,'a') as file:
        for hijo in range(args.number):
            char = char % 26
            hijo = os.fork()
            hijo_char = chr(char+65)
            char += 1
            if hijo == 0:
                for rep in range(args.repeat):
                    if args.verb:
                        sp.Popen(['echo Proceso '+str(os.getpid())+' escribiendo letra '+hijo_char],shell=True,stdout=file)
                    else:
                        sp.Popen(['echo','-n',hijo_char],stdout=file)
                    file.flush()
                    time.sleep(1)
                sys.exit()   
        for hijo in range(args.number):
            os.wait()
        sp.Popen(['echo',''],stdout=file) #imprime un salto de linea, para separar los outputs anteriores
        proc = sp.Popen(['cat',args.file])


if __name__ == '__main__':
    main()