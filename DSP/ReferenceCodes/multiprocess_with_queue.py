# Example of multiprocessing usage with queue

import multiprocessing
import time

def reader(queue):
    name = multiprocessing.current_process().name
    print ("--------",name, 'Starting',"--------")
    while True:
        if(not queue.empty()): print("Queue value: ",queue.get())
        else: print("Waiting for queue...")
        time.sleep(0.5)

def writer(queue):
    name = multiprocessing.current_process().name
    print ("--------",name, 'Starting',"--------")
    counter=0
    while True:
        queue.put(counter)
        counter=counter+1
        time.sleep(1)


if __name__ == '__main__':

    queue = multiprocessing.Queue()

    read_inst = multiprocessing.Process(name='Reader', target=reader  ,args=[queue])
    write_inst = multiprocessing.Process(name='Writer', target=writer ,args=[queue])

    read_inst.start()
    write_inst.start()