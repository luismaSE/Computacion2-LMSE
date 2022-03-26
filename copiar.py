#Escribir un programa que reciba dos nombres de archivos 
# por línea de órdenes utilizando los parámetros “-i” y “-o” procesados con argparse.

#l programa debe verificar que el archivo pasado a “-i” exista en el disco.
# De ser así, lo abrirá en modo de solo lectura, leerá su contenido, y copiará dicho contenido en un archivo nuevo cuyo nombre será el pasado a “-o”.
#  Si el archivo nuevo ya existe, deberá sobreescribirlo.

#Ejemplo:

#python3 copiar.py -i existente.txt -o nuevo.txt

import argparse
from os.path import exists

def main():
    parser = argparse.ArgumentParser(description='Lee el contenido de un archivo, luego copiará dicho contenido en un archivo nuevo')
    parser.add_argument('-i',required=True,help='Archivo de Origen')
    parser.add_argument('-o',required=True,help='Archivo de destino')
    arguments = parser.parse_args()
    
    ok = True
    if exists(arguments.o):
        print('El archivo de destino ya existe, desea sobreescribirlo?')
        if str(input('(Presione ENTER para confirmar, ingrese cualquier otra tecla para cancelar)')) != '':
            ok = False
    if ok:
        with open(arguments.i,'r') as ifile:
            with open(arguments.o, 'w') as ofile:
                ofile.write(ifile.read())
                print(arguments.i,'---copiando--->',arguments.o)
                print('Operación realizada con exito')
    else:
        print('Operacion cancelada')

if __name__=='__main__':
    main()