import time
from Routes import Routes


class RoutingTable:
    def __init__(self, id):
        self.routerID = id
        self.routes = []
        self.neighbours = []
        self.deadneighbours = []

        self.routes.append(Routes(self.routerID, self.routerID, 0, 1))

    def getRoutes(self):
        return self.routes

    def setNeighbours(self, n):
        self.neighbours = n

    def processRoute(self, route):

        receivedDestDown = False

        if (route.dest == route.origen):
            self.processNeighbour(route)

        haveRoute = False
        for r in self.routes:
            if (r.dest == route.dest):
                haveRoute = True
                if route.numHops < r.numHops and route.origen == r.origen:
                    self.routes.remove(r)
                    self.routes.append(route)

                    if route.origen == r.origen and route.numHops == 16 and r.numHops != 16:
                        receivedDestDown = True

        if not haveRoute:
            self.routes.append(route)

        return receivedDestDown

    def processNeighbour(self, neighbour):
        timeNow = time.time()
        isNew = True
        for n in self.neighbours:
            if n[0] == neighbour.dest:
                if (self.deadneighbours.count(neighbour.dest) > 0):
                    self.deadneighbours.remove(neighbour.dest)
                self.neighbours.remove(n)
                self.neighbours.append((neighbour.dest, timeNow))
                isNew = False
        if isNew:
            self.neighbours.append((neighbour, timeNow))

    def checkNeighbours(self, router):
        if router.getStatus() == 0:
            for route in self.routes:
                if int(route.dest) == int(router.getID()):
                    route.numHops = 16

            if self.routerID != router.getID():
                self.printTable()
                self.checkScope(router)
                return True
        return False

    def getNeighbours(self):
        self.neighbours.sort()
        return [n[0] for n in self.neighbours]

    def checkScope(self, router):
        for rs in router.getTable().getRoutes():
            for route in self.routes:
                #print(self.neighbours)
                if int(route.dest) == int(rs.dest) and not( rs.dest in self.neighbours) and rs.dest != self.routerID:
                    route.numHops = 16

    def getDeadNeighbours(self):
        return self.deadneighbours

    def printTable(self):
        print("Dest\t| Address\t| NumHops")
        print("-------------------------------------------")
        for route in self.routes:
            if (route.numHops != 16):
                formattednumHops = str(route.numHops)
            else:
                formattednumHops = "inf"
            print("{}\t|  {}\t|  {}".format(route.dest, route.address, formattednumHops))
