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
import os

def h1(child1,q):
    while True:
        inp = os.read(0,1024)
        child1.send(inp)
        if inp == b'\n':
            break
        print(q.get().decode())
        
    inp = q.get()

    while inp != b'':
        os.write(1,inp)
        inp = q.get()


def h2(child2,q):
    uncoded = child2.recv().decode()
    while uncoded != '\n':
        rot = rot13(uncoded)
        q.put(rot.encode())
        uncoded = child2.recv().decode()
    q.put(b'')


def rot13(uncoded):
    coded = ''
    for char in uncoded:
        if char.isalpha():
            if char.isupper():
                coded += chr(((ord(char.lower())-97+13)%26)+97).upper()
            else:
                coded += chr(((ord(char)-97+13)%26)+97)
        else:
            coded += char
    return coded



if __name__ == '__main__':
    child1 , child2 = mp.Pipe()
    q = mp.Queue()
    p1 = mp.Process(target=h1,args=(child1,q))
    p2 = mp.Process(target=h2,args=(child2,q))
    p1.start()
    p2.start()
    p1.join()
    p2.join()