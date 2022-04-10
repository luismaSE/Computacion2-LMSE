#!/usr/bin/python
import argparse
import os
import sys

def suma():
    sum = 0
    total = os.getpid()
    for num in range(total+1):
        if num % 2 == 0:
            sum += num
    return sum

def main():
    parser = argparse.ArgumentParser(description=
    'El programa genera n procesos hijos, cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID')
    parser.add_argument('-n','--number',type=int,required=True,help='numero de procesos hijos que se van a crear')
    parser.add_argument('-v', '--verb',action='store_true',help='activa el modo verboso')
    args = parser.parse_args()

    for loop in range(args.number):
        hijo = os.fork()
        if hijo == 0:
            if args.verb:
                print('Starting Process:%d\n'%os.getpid())
            print(os.getppid(),'-',os.getpid(),':',suma())
            if args.verb:
                print('Ending Process: %d\n'%os.getpid())
            sys.exit()
    for hijo in range(args.number):
        os.wait()

if __name__ == '__main__':
    main()