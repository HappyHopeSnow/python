from queue import Queue
from threading import Thread


def produce(q):
    i = 0
    while(True):
        print('produce: ' + str(i))
        q.put(i)
        i += 1
        
def comsume(q):
    while(True):
        data = q.get()
        print('consume: ' + str(data))


def main():
    q = Queue()
    t1 = Thread(target=produce, args=(q,))
    t2 = Thread(target=comsume, args=(q,))
    t1.start()
    t2.start()
    
    
if __name__ == '__main__':
    main()