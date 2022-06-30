import queue
import threading
import time



class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)



exitFlag=0
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []
segments = []#[[4,"flow3.mp4",0,30,DIVIDER1,DIVIDER2,DIVIDER3,DIVIDER4,DIVIDER5,DIVIDER6],[1,"flow.mp4",10,20,DIVIDER1,DIVIDER2,DIVIDER3,DIVIDER4,DIVIDER5,DIVIDER6],[2,"flow2.mp4",0,10,DIVIDER1,DIVIDER2,DIVIDER3,DIVIDER4,DIVIDER5,DIVIDER6],[3,"flow3.mp4",20,30,DIVIDER1,DIVIDER2,DIVIDER3,DIVIDER4,DIVIDER5,DIVIDER6]]
nthreads=2
counter_list={}

threadID =1
def start():
    # Create new threads
    global threadID
    global exitFlag
    for t in range(1,nthreads+1,1):
        tName="Thread-"+str(t)
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)

        threadID += 1

    # Fill the queue
    queueLock.acquire()
    for word in segments:
        workQueue.put(word)
    queueLock.release()


    # Wait for queue to empty
    while not workQueue.empty():
        time.sleep(1)
        pass


    # Notify threads it's time to exit
    exitFlag = True
    # Wait for all threads to complete
    for t in threads:
        t.join()



    print("Exiting Main Thread")


def stop(self):
    return 0
import count

def process_data(threadName, q):
    global counter_list
    global exitFlag
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (threadName, data))
            [id,vid,st,en,d1,d2,d3,d4,d5,d6,min,max]=data

            #count1 =count.counter()
            #count1.co(vid, st, en, d1, d2, d3, d4, d5, d6)
            c={id:count.count(vid, st, en, d1, d2, d3, d4, d5, d6,id,min,max) }
            counter_list[id]=c[id]
        else:
            queueLock.release()
        #time.sleep(1)

def start_classify():
    f=1
    import time
    while (f==1):
        time.sleep(1)
        with open('clossify','r') as fi:
            f=int(fi.read())
            fi.close()
    with open('clossify','w') as fi:
            fi.write('1')
            fi.close()
def stop_classify():
    with open('clossify','w') as fi:
            fi.write('1')
            fi.close()