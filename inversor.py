'''
Contenido del archivo /tmp/texto.txt

Hola Mundo
que tal
este es un archivo
de ejemplo.
'''
import argparse , os , sys , fcntl , time

def main():
    parser = argparse.ArgumentParser(description=
    '''
    El programa abre el archivo de texto indicado.
    Luego genera tantos hijos como lineas tenga dicho archivo.
    Cada hijo invertira una linea de texto y se la devuelve al padre
    Por ultimo, el padre devuelve todo el texto invertido por pantalla
''')
    parser.add_argument('-f','--file',required=True,type=str,help='archivo de texto')
    args = parser.parse_args()
    
    r,w = os.pipe() ; r1,w1 = os.pipe()
    #fcntl.fcntl(r1, fcntl.F_SETFL, os.O_NONBLOCK)
    with open(args.file, 'r') as file:
        text = file.readlines() ; num = len(text) ; child = 1
    for _ in range(num):
        if child != 0:
            child = os.fork()

    if child == 0:  #  ----------------------------------->  Zona de los Hijos
        os.close(w1) ; os.close(r)
        with os.fdopen(w, 'w') as w , os.fdopen(r1) as r1:
            string = '' ; new_string = ''
            while string == '':
                string = r1.readline()
            for char in reversed(string): 
                new_string += char
            w.write(new_string) ; w.flush() ; w.close()
        sys.exit()

    os.close(w) ; os.close(r1)
    with os.fdopen(w1,'w') as w1:
        for _ in range(num):
            w1.write(text[_]) ; time.sleep(0.1) ; w1.flush()
        
    for child in range(num):
        os.wait()
    with os.fdopen(r) as r:
        print(r.read())

if __name__ == "__main__":
    main()