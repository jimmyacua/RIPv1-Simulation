import threading
import time
import sys
from datetime import datetime
from socket import *


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        # threadLock.acquire()
        clientSide(self.threadID)
        # Free lock to release next thread
        # threadLock.release()


def clientSide(i):
    serverIP = "127.0.0.1"
    serverPort = 8999

    port = 0
    if i == 1:
        port = 8971
    elif i == 2:
        port = 8972
    elif i == 3:
        port = 8973
    elif i == 4:
        port = 8974
    elif i == 5:
        port = 8975

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.bind(('', port))
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    message = "mensaje " + str(i)
    clientSocket.sendto(message.encode(), (serverIP, serverPort))
    sem = threading.Semaphore()
    sem.acquire()
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(i, "received", modifiedMessage)  # print the received message
    clientSocket.close()  # Close the socket
    sem.release()

# threadLock = threading.Lock()
threads = []

# Create new threads
r1 = myThread(1, "router 1", 1)
r2 = myThread(2, "router 2", 1)
r3 = myThread(3, "router 3", 1)
r4 = myThread(4, "router 4", 1)
r5 = myThread(5, "router 5", 1)
# Start new Threads

lock = threading.Lock()
lock.acquire()
r1.start()

r2.start()

r3.start()

r4.start()

r5.start()
lock.release()

# Add threads to thread list

threads.append(r1)
threads.append(r2)
threads.append(r3)
threads.append(r4)
threads.append(r5)

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")
