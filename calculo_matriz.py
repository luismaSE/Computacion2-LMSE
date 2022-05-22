#!/usr/bin/python
'''
Suponiendo que el archivo /tmp/matriz.txt tenga este contenido:

1, 2, 3

4, 5, 6

python3 calculo_matriz -f /tmp/matriz.txt -p 4 -c pot

1, 4, 9

16, 25, 36
'''
from sympy import *
from cmath import sqrt , log10
import argparse
import multiprocessing as mp


def crear_file():
    file = open('/tmp/matriz.txt','w+')
    file.write(
'''1, 2, 3
4, 5, 6''')


def crear_matriz(file):
    mat = []
    text = file.readlines()
    for line in text:
        new_line = []
        for char in line:
            if char.isnumeric():
                new_line.append(int(char))        
        mat.append(new_line)
    return mat


def raiz(num):
    return sqrt(num)

def pot(num):
    return num**2

def log(num):
    return log10(num)


def main():
    parser = argparse.ArgumentParser(description=
    '''
    El programa lee una matriz almacenada en un archivo de texto pasado 
    por argumento -f, y calcula la una de 3 operaciones posibles para cada uno de sus elementos.

    Las 3 operaciones posibles son:

    raiz: calcula la raíz cuadrada del elemento.
    pot: calcula la potencia del elemento elevado a si mismo.
    log: calcula el logaritmo decimal de cada elemento.
    ''')
    parser.add_argument('-p','--process')
    parser.add_argument('-f','--file')
    parser.add_argument('-c','--calc')
    args = parser.parse_args()
    with open(args.file) as file:
        mat = crear_matriz(file)
    new_mat = []
    pool = mp.Pool(processes=int(args.process))
    for line in mat:
        if args.calc == 'raiz':
            new_mat.append(pool.map(raiz,line))
        elif args.calc == 'pot':
            new_mat.append(pool.map(pot,line))
        elif args.calc == 'log':
            new_mat.append(pool.map(log,line))
    
    matriz = Matrix(new_mat)
    pprint(matriz)
if __name__ == '__main__':
    crear_file()
    main()