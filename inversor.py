'''
Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.

    El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
    El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un child.
    Cada child deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
    El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.

Ejemplo:

Contenido del archivo /tmp/texto.txt
Hola Mundo
que tal
este es un archivo
de ejemplo.

Ejecución:

python3 inversor.py -f /tmp/texto.txt

ovihcra nu se etse
.olpmeje ed
lat euq
odnuM aloH'''


import argparse
import subprocess as sp
import os
import sys

def main():
    parser = argparse.ArgumentParser(description=':D')
    parser.add_argument('-f','--file',required=True,type=str,help='archivo de texto')
    args = parser.parse_args()
    
    i = 0
    with open(args.file, 'r') as file:
        text = file.readlines() ; num = len(text)
    for _ in range(num):
        r,w = os.pipe() ; child = os.fork()

        if child == 0:  #  ----------------------------------->  Zona del Hijo
            os.close(r)
            w = os.fdopen(w, 'w')
            string = text[i] 
            new_string = ''
            for char in reversed(string): 
                if char != '\n': 
                    new_string += char
            w.write(new_string)
            w.close() ; sys.exit() #  ------------------------>  Fin del proceso Hijo

        i += 1
        os.close(w)
        r = os.fdopen(r)
        print(r.read())
    r.close()
        
    for child in range(num):
        os.wait()

if __name__ == "__main__":
    main()