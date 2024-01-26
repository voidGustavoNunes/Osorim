from threading import Thread
from time import sleep, time
from sys import exit

t_init = time()
i=0

def aux(name) :
        t_func = time() - t_init
        print(f'Thread: starting at {t_func}s')
        print(f'Thread {name}\n')
        sleep(10)
        print(f'Thread {name} ending\n')
        return 1

if __name__ == "__main__":
        try :
            while(1) :
                x = Thread(target=aux, args=(i,))

                x.start()
                i+=1
                sleep(5)
                print(x)
                
        except KeyboardInterrupt:
            print(f"Finalizando {i} Threads após {time()-t_init}s")
