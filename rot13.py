#!/usr/bin/python
'''
Escribir un programa que genere dos hijjos utilizando multiprocessing.
Uno de los hijos deberá leer desde stdin texto introducido por el usuario,
 y deberá escribirlo en un pipe (multiprocessing).
El segundo hijo deberá leer desde el pipe el contenido de texto, 
lo encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).
El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.
'''
import multiprocessing as mp
import sys , os , time


def main():
    #mp.set_start_method('spawn')
    pass


def h1(child1,q):
    child1.send(inp)
    child1.close()
    print(q.get(),'\n')


def h2(child2,q):
        coded = ''
        uncoded = child2.recv()
        print('UNCODED=',uncoded)
        for char in uncoded:
            if char.isalpha():
                coded += chr(((ord(char)-97+13)%26)+97)
            else:
                coded += char
        q.put(coded)



if __name__ == '__main__':
    child1 , child2 = mp.Pipe()
    q = mp.Queue()
    inp = str(input()).lower()
    p1 = mp.Process(target=h1,args=(child1,q))
    p2 = mp.Process(target=h2,args=(child2,q))
    p1.start()
    p2.start()
    os.wait()
    p1.join()
    p2.join()