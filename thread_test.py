from threading import Thread, Lock
import time 
import queue

mutex = Lock()

def processData(queue):
    run = True
    counter = 0
    while run:
        mutex.acquire()
        print("Thread acquired mutex")
        counter += 1
        try:
            for i in range(1, 15):
                queue.put(i)
        finally:
            print("Thread released mutex")
            mutex.release()
            time.sleep(0.01)
        if (counter == 3):
            run = False
            break
    return


q = queue.Queue()
t1 = Thread(target = processData, args = (q, ))
t1.start()
go = True
j = 0
while go:
    mutex.acquire()
    print("Main thread acquired mutex")
    j+=1
    for i in range(q.qsize()):
        item = q.get()
        print(f"Item {i}: {item}")
    print("Main thread released mutex")
    mutex.release()
    time.sleep(0.01)
    if (j == 3):
        go = False

print("Main thread finished, waiting for child")
t1.join()
print("Joind successfully, ending")







