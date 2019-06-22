import pickle
import socket
import time
import threading


from Router import Router
from Routes import Routes

updatePeriod = 10
timeout = 20

# initialice the routers

r1 = Router(1, ["192.168.0.1"], [["192.168.0.2", 3, 2]])
r2 = Router(2, ["192.168.0.12"], [["192.168.0.18", 3, 2]])
r3 = Router(3, ["192.168.0.2", "192.168.0.5", "192.168.0.18", "192.168.0.13"],
            [["192.168.0.1", 1, 2], ["192.168.0.12", 2, 2], ["192.168.0.6", 4, 2], ["192.168.0.14", 5, 2]])
r4 = Router(4, ["192.168.0.6", "192.168.0.9"], [["192.168.0.5", 3, 2], ["192.168.0.10", 5, 2]])
r5 = Router(5, ["192.168.0.10", "192.168.0.14"], [["192.168.0.13", 3, 2], ["192.168.0.9", 4, 2]])

r1.addNeighbour(3)
r1.getTable().setNeighbours(r1.getNeighbours())

r2.addNeighbour(3)
r2.getTable().setNeighbours(r2.getNeighbours())
r3.addNeighbour(1)
r3.addNeighbour(2)
r3.addNeighbour(4)
r3.addNeighbour(5)
r3.getTable().setNeighbours(r3.getNeighbours())
r4.addNeighbour(3)
r4.addNeighbour(5)
r4.getTable().setNeighbours(r4.getNeighbours())
r5.addNeighbour(3)
r5.addNeighbour(4)
r5.getTable().setNeighbours(r5.getNeighbours())

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
            if (r.getOutputPorts()[i][1] == n):
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

messages = []

timeToKill = time.time() + 60


def sendRequest(router, route):
    outPorts = router.getOutputPorts()
    lista = []
    for r in route:
        rou = Routes(r.origen, r.dest, r.address, r.numHops)
        lista.append(rou)
    toSend = pickle.dumps((lista, router.getID(), "REQUEST"))

    for (outPort, outRouterID, numHops) in outPorts:
        p = str(outPort).split(".")
        # lock.acquire()
        # outsocket.sendall(toSend)
        outsocket.sendto(toSend, ('127.0.0.1', 8000 + int(p[3])))
        # lock.release()

    # print("end sending request packet")


def sendUpdate(router, route, target=None):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        p = str(outPort).split(".")
        if target == None or target == outRouterID:
            outRoutes = []
            for r in route:

                # poison reverse
                if r.origen == outRouterID:
                    r = Routes(r.dest, r.origen, r.address, 16)
                if not r.dest == outRouterID:
                    outRoutes.append(r)

                toSend = pickle.dumps((outRoutes, router.getID(), "UPDATE"))

                outsocket.sendto(toSend, ('127.0.0.1', 8000 + int(p[3])))


def getOutputPortTo(router, dest):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        if int(outRouterID) == dest:
            return outPort
    return 1111


def getHopsTo(router, dest):
    outPorts = router.getOutputPorts()
    for (outPort, outRouterID, numHops) in outPorts:
        if int(outRouterID) == int(dest):
            return numHops
    return 16


def rip(router):
    timeToLive = time.time()

    for port in router.getInputPorts():
        portSplit = str(port).split(".")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inputSockets.append(sock)
        sock.bind(('127.0.0.1', 8000 + int(portSplit[3])))

    sendRequest(router, router.getTable().getRoutes())

    while True:
        sendUpdate(router, router.getTable().getRoutes())
        startTime = time.time()
        blockduration = 0

        while blockduration < updatePeriod:
            inputs = inputSockets
            updateRequired = False
            for insock in inputs:
                message = insock.recv(4096)
                s = pickle.loads(message)
                for r in s[0]:
                    rout = r
                    if "REQUEST" in s:
                        sendUpdate(router, router.getTable().getRoutes(), rout.dest)

                    else:
                        for route in s[0]:
                            newNumHops = 0
                            if routers[route.dest - 1].getStatus() == 0:
                                newNumHops = 16
                            else:
                                newNumHops = min(int(route.numHops) + int(getHopsTo(router, route.origen) - 1), 16)

                            route = Routes(router.getID(), route.dest, route.address, newNumHops)

                            updateRequired = router.getTable().processRoute(route)

                timeToLive = time.time()
                #print("TIME", timeToLive)
                if timeToLive >= timeToKill:
                    routers[2].shutdown()
                    if router.getID() == 3:
                        print("R3 IS DOWN")
                        time.sleep(3600)

                for dr in routers:
                    updateRequired = router.getTable().checkNeighbours(dr)
                    if updateRequired:
                        sendUpdate(router, router.getTable().getRoutes())

            blockduration = time.time() - startTime

            if router.getStatus() == 1:
                print("Routing table of router", router.getID())
                router.getTable().printTable()
            time.sleep(10)


class myThread(threading.Thread):
    def __init__(self, router):
        threading.Thread.__init__(self)
        self.router = router

    def run(self):
        print("Starting thread " + str(self.router.getID()))
        rip(self.router)


if __name__ == "__main__":
    r = input("Digite el router \n")
    rip(routers[int(r) - 1])

    # rip(r1)
    # rip(r2)
    # rip(r3)
    # rip(r4)
    # rip(r5)

    '''t1 = myThread(r1)
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

    for t in threads:
        t.join()'''

    # outsocket.close()
    # for soc in inputSockets:
    #   soc.close()
