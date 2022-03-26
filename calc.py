import getopt
import sys

class Error_rep(Exception):
    pass

def calc(o,n1,n2):
    if o == '+':
        res = int(n1) + int(n2)
    if o == '-':
        res = int(n1) - int(n2)
    if o == '*':
       res = int(n1) * int(n2)
    if o == '/':
        res = int(n1) / int(n2)

    print(n1,o,n2,'=',res)    
            

def main():
    try:
       
        (optlist,args) = getopt.getopt(sys.argv[1:],'m:n:o:',[])
        print(optlist)
        for op , ar in optlist:
            #print('optlist: ',optlist)
            #print('op: ',op)
            #print(s.count(op))
            print('op:',op,'  contador:',str(optlist).count(op))
            if str(optlist).count(op) > 1:
               raise Error_rep
            if op == '-n':
                n1 = ar
            if op == '-m':
                n2 = ar
            if op == '-o':
                operacion = ar
        calc(operacion,n1,n2)
    except getopt.GetoptError as e:
        print(e)
    except Error_rep:
        print('comando Repetido')
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()