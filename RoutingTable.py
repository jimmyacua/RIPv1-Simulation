import time
from Routes import Routes

class RoutingTable:
    def __init__(self, id):
        self.routerID = id
        self.routes = []

        self.routes.append(Routes(self.routerID, self.routerID, 0,1))

    def getRoutes(self):
        return self.routes


    def processRoute(self, route):

        receivedDestDown = False

        #route.printRoute()

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
        #print("finaliza")
        return receivedDestDown

    def printTable(self):
        #self.routes.sort(self.routes.dest)

        print("Dest\t| origen\t| Address\t| NumHops")
        print("-------------------------------------------")
        for route in self.routes:
            if (route.numHops != 16):
                formattednumHops = str(route.numHops)
            else:
                formattednumHops = "inf"
            print("{}\t| {}\t\t|  {}\t|  {}".format(route.dest, route.origen, route.address, formattednumHops))
