import subprocess
import argparse

#Ejemplos
#python ejecutor.py -c "ip a" -o /tmp/salida -l /tmp/log
#python ejecutor.py -c "ls /cualquiera" -o /tmp/salida -l /tmp/log

def main():
    parser = argparse.ArgumentParser(description='Hola :D')
    parser.add_argument('-c','--command')
    parser.add_argument('-o','--output_file')
    parser.add_argument('-l','--log')
    args = parser.parse_args()

    with open(args.output_file,'w') as output, open(args.log,'a') as log:
        c = subprocess.Popen(args.command.split(),stdout=output,stderr=subprocess.PIPE)
        error= c.communicate()[1]
        if error != b'':
            string = 'echo -e $(date +%D-%T): '+str(error)
        else:
            string = 'echo $(date +%D-%T): Comando: '+str(args.command)+' Ejecutado correctamente ; echo -e\n'
        subprocess.Popen([string],shell=True,stdout=log)

if __name__=='__main__':
    main()