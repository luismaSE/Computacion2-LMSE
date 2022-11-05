from cmath import sqrt , log10
import click

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


@click.command()
@click.option('-f',default='RUTA',help='Archivo de texto')
@click.option('-c',default='pot',help="""(pot)
                                         (raiz)
                                         (log)
                                         """)

def main():
    pass

if __name__ == '__main__':
    main():
