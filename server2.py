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
        serverSide()
        # Free lock to release next thread
        # threadLock.release()


def serverSide():
    serverPort1 = 8999
    serverPort2 = 8972
    serverPort3 = 8973
    serverPort4 = 8974
    serverPort5 = 8975
    serverIP = '127.0.0.1'

    lock = threading.Lock()
    lock.acquire()
    serverSocket1 = socket(AF_INET, SOCK_DGRAM)
    serverSocket1.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverSocket1.bind((serverIP, serverPort1))
    lock.release()

    '''lock.acquire()
    serverSocket2 = socket(AF_INET, SOCK_DGRAM)
    serverSocket2.bind((serverIP, serverPort2))
    lock.release()

    lock.acquire()
    serverSocket3 = socket(AF_INET, SOCK_DGRAM)
    serverSocket3.bind((serverIP, serverPort3))
    lock.release()

    lock.acquire()
    serverSocket4 = socket(AF_INET, SOCK_DGRAM)
    serverSocket4.bind((serverIP, serverPort4))
    lock.release()

    lock.acquire()
    serverSocket5 = socket(AF_INET, SOCK_DGRAM)
    serverSocket5.bind((serverIP, serverPort5))
    lock.release()'''
    print("SERVER HERE!\nThe server is ready to receive")
    while 1:

        message, clientAddress = serverSocket1.recvfrom(2048)
        print("mensaje:", message)
        modifiedMessage = message.upper()
        port = 8970
        sem = threading.Semaphore()
        sem.acquire()
        for i in range(1,6):
            port += 1
            serverSocket1.sendto(modifiedMessage, ('<broadcast>', port))
        sem.release()

        '''message, clientAddress = serverSocket2.recvfrom(2048)
        print(message)
        modifiedMessage = message.upper()
        serverSocket1.sendto(modifiedMessage, clientAddress)

        message, clientAddress = serverSocket3.recvfrom(2048)
        print(message)
        modifiedMessage = message.upper()
        serverSocket1.sendto(modifiedMessage, clientAddress)

        message, clientAddress = serverSocket4.recvfrom(2048)
        print(message)
        modifiedMessage = message.upper()
        serverSocket1.sendto(modifiedMessage, clientAddress)

        message, clientAddress = serverSocket5.recvfrom(2048)
        print(message)
        modifiedMessage = message.upper()
        serverSocket1.sendto(modifiedMessage, clientAddress)'''


threads = []

# Create new threads
thread1 = myThread(1, "Thread-1", 1)

thread1.start()

threads.append(thread1)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting Main Thread")