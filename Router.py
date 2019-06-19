from RoutingTable import RoutingTable
class Router:
    def __init__(self, id, inports, outports):
        self.routerID = id
        self.inputPorts = inports

        #destPort-routerID-numHops
        self.outputPorts = outports
        self.routingTable = RoutingTable(id)
        self.neighbours = []

    def getID(self):
        return self.routerID

    def getTable(self):
        return self.routingTable

    def getNeighbours(self):
        return self.neighbours

    def addNeighbour(self, n):
        self.neighbours.append(n)

    def removeNeighbour(self, n):
        self.neighbours.remove(n)

    def getOutputPorts(self):
        return self.outputPorts