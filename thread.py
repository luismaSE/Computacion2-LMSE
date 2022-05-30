'''
Escribir un programa que genere dos hilos utilizando threading.

Uno de los hilos deberá leer desde stdin texto introducido por el usuario, 
y deberá escribirlo en un mecanismo IPC (*).

El segundo hijo deberá leer desde dicho mecanismo IPC el contenido de texto,
 lo encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola de mensajes (queue).

El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

(*) Verificar si el uso de os.pipe(), named pipes, o multiprocessing.Pipe() son thread-safe, 
caso contrario usar Queue.
'''

import threading, os, queue

def h1():
    inp = os.read(0,1024).decode()
    q.put(inp)
    print(q2.get())

def h2():
    q2.put(rot13(q.get()))

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

def main():
    threading.Thread(target=h1,daemon=False).start()
    threading.Thread(target=h2,daemon=False).start()
    q2.join()
    
if __name__=='__main__':
    q = queue.LifoQueue()
    q2 = queue.LifoQueue()
    main()
