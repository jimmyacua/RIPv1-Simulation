import socket
import time
import threading

from Router import Router
from Routes import Routes

updatePeriod = 10
timeout = 20

#initialice the routers

r1 = Router(1, ["192.168.0.1"], [["192.168.0.2",3,2]])
r2 = Router(2, ["192.168.0.12"], [["192.168.0.18",3,2]])
r3 = Router(3, ["192.168.0.2", "192.168.0.5", "192.168.0.18", "192.168.0.13"], [["192.168.0.1",1,2], ["192.168.0.12",2,2], ["192.168.0.6",4,2], ["192.168.0.14",5,2]])
r4 = Router(4, ["192.168.0.6", "192.168.0.9"], [["192.168.0.5",3,2], ["192.168.0.10",5,2]])
r5 = Router(5, ["192.168.0.10", "192.168.0.14"], [["192.168.0.13",3,2], ["192.168.0.9",4,2]])

r1.addNeighbour(3)
r2.addNeighbour(3)
r3.addNeighbour(1)
r3.addNeighbour(2)
r3.addNeighbour(4)
r3.addNeighbour(5)
r4.addNeighbour(3)
r4.addNeighbour(5)
r5.addNeighbour(3)
r5.addNeighbour(4)

routers = []

routers.append(r1)
routers.append(r2)
routers.append(r3)
routers.append(r4)
routers.append(r5)

for r in routers:
    neigh = r.getNeighbours()
    for n in neigh:
        index = 0
        for i in range(5):
            if(r.getOutputPorts()[i][1] == n):
                index = i
                break
        route = Routes(r.getID(), n, r.getOutputPorts()[index][0], r.getOutputPorts()[index][2])
        r.getTable().processRoute(route)
    print("INITIAL ROUTING TABLES")
    print("Routing Table of router", r.getID())
    r.getTable().printTable()
    print("-----------------------------------------------------------------------------")

inputSockets = []

outsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sendRequest(router):
    outPorts = router.getOutputPorts()
    #print("sending request packet")
    message = str(router.getID()) + ", " + str(outPorts) + "REQUEST"
    for (outPort, outRouterID, numHops) in outPorts:
        lock.acquire()
        outsocket.sendto(message.encode(), ('127.0.0.1', 8000+int(outPort[10])))
        #print("sendREq", 8000+int(outPort[10]))
        lock.release()

    #print("end sending request packet")

def sendUpdate(router, target = None):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        #print(outPort, outRouterID, numHops)
        if target == None or target == outRouterID:
            outRoutes = []
            for r in router.getTable().getRoutes():
                #poison reverse
                if r.origen == outRouterID:
                    r = Routes(r.dest, r.origen, r.address, 16)
                if r.dest != outRouterID:
                    outRoutes.append(r)

                message = str(router.getID()) + "," + str(outRoutes) + "," + "UPDATE"
                lock.acquire()
                outsocket.sendto(message.encode(), ('127.0.0.1', 8000+int(outPort[10])))
                lock.release()

def getOutputPortTo(router, dest):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        if int(outRouterID) == dest.getID():
            return outPort
    return 0

def getHopsTo(router, dest):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        if outRouterID == dest.getID():
            return numHops
    return 16

lock = threading.Lock()

def rip(router):
    for port in router.getInputPorts():
        portSplit = str(port).split(".")
        lock.acquire()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #print(port, port[10])
        inputSockets.append(sock)
        #print(8000 + int(port[10]))
        sock.bind(('127.0.0.1', 8000+int(portSplit[3])))
        #print("binded")
        lock.release()


    sendRequest(router)
    #print("sale sendReq")

    while True:
        sendUpdate(router)
        #print("sale sedUpda")
        startTime = time.time()
        blockduration = 0

        while blockduration < updatePeriod:
            inputs = inputSockets
            updateRequired = False

            for insock in inputs:
                message = insock.recv(1024)
                #print(message[1])
                messageString = str(message)
                message = messageString.split(",")
                #print(message[0])
                #print(len(message[0]))
                if "REQUEST" in messageString:
                    #print("REQUEST RECEIVED FROM", messageString[2])
                        sendUpdate(router,  messageString[2])
                else:
                    #print(messageString)
                    #print("AQUI", messageString[0])
                    r = 0
                    if len(message[0]) != 1:
                        r = 2
                    outP = routers[(int(message[0][r]))-1].getOutputPorts()
                    for route in outP:
                        #newOutPort = getOutputPortTo(routers[int(message[2]-1)])
                        #print("ruta", route)
                        newOutPort = getOutputPortTo(router, routers[route[1] -1])
                        newNumHops = min(int(route[2]) + int(getHopsTo(router, routers[route[2]])),  16)
                        route = Routes(router.getID(), route[1], newOutPort, newNumHops)
                        #print("ruta", route.dest, , route.numHops)

                        router.getTable().processRoute(route)

                #router.getTable().printTable()


            blockduration = time.time() - startTime

            print("Routing table of router", router.getID())
            router.getTable().printTable()
            time.sleep(10)
            #lock.release()

            #time.sleep(10)


class myThread(threading.Thread):
    def __init__(self, router):
        threading.Thread.__init__(self)
        self.router = router

    def run(self):
        print("Starting thread " + str(self.router.getID()))
        # Get lock to synchronize threads
        # threadLock.acquire()
        rip(self.router)

        # Free lock to release next thread
        # threadLock.release()

if __name__ == "__main__":
    '''r = input("router?\n")
    rip(routers[int(r)-1])'''
    #rip(r1)
    #rip(r2)
    #rip(r3)
    #rip(r4)
    #rip(r5)

    t1 = myThread(r1)
    t2 = myThread(r2)
    t3 = myThread(r3)
    t4 = myThread(r4)
    t5 = myThread(r5)

    threads = []
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    threads.append(t5)


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    #for t in threads:
      #  t.join()

    #outsocket.close()
    #for soc in inputSockets:
     #   soc.close()


