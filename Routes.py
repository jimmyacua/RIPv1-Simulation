class Routes:
    def __init__(self, origen, dest, address, numHops):
        self.origen = origen
        self.dest = dest
        self.address = address
        self.numHops = numHops

    def printRoute(self):
        print(self.origen, self.dest, self.address, self.numHops)