import click
from sympy import *
from celery_config import app
from math import sqrt , log10


def funcion_calculo(c,num):
    if c == 'raiz':
        return raiz.delay(num)
    elif c == 'pot':
        return pot.delay(num)
    elif c == 'log':
        return log.delay(num)

@app.task
def raiz(num):
    return sqrt(num)

@app.task
def pot(num):
    return num**2

@app.task
def log(num):
    return log10(num)

def crear_file():
    file = open('/tmp/matriz.txt','w+')
    file.write(
'''1, 2, 3
4, 5, 6''')

def crear_matrices(file):
    mat = []
    new_mat = []
    text = file.readlines()
    for row in text:
        line = []
        new_line = []
        for char in row:
            if char.isnumeric():
                line.append(int(char))
                new_line.append(0)

        mat.append(line)
        new_mat.append(new_line)
    return mat,new_mat

@click.command()
@click.option('-f',default='/tmp/matriz.txt',help='Archivo de texto')
@click.option('-c',default='pot', 
                   type=click.Choice(['pot', 'log','raiz'], 
                   case_sensitive=False),
                   help='''Ingresar:\n
                            (pot) para calcular potencia de 2\n
                            (raiz) para calcular raiz cuadrada\n
                            (log) para calcular logaritmo''')
                                         
def main(f,c):
    with open(f) as file:
        mat,new_mat = crear_matrices(file)
    for row in range(len(mat)):
        for col in range(len(mat[row])):
            new_mat[row][col] = funcion_calculo(c,mat[row][col]).get()
    matriz = Matrix(new_mat)
    pprint(matriz)


if __name__ == '__main__':
    crear_file()
    main()
