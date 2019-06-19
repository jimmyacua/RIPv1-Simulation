import socket
import time


class Subred:
    def __init__(self, ip, mas):
        self.ipAddress = ip
        self.mask = mas

class Client:
    listRouters = []
    connections = {}
    listSubredes = {}

    def main(self):
        global listSubredes
        subnet1 = Subred('10.0.1.0', '255.255.255.0')
        subnet4 = Subred('10.0.2.0', '255.255.255.0')
        subnet2 = Subred('10.0.3.0', '255.255.255.0')
        subnet5 = Subred('10.0.4.0', '255.255.255.0')
        subnet3 = Subred('0.0.0.0', '255.255.255.0')

        listSubredes = {'1': subnet1, '2': subnet2, '3': subnet3, '4': subnet4, '5': subnet5}
        routers = []
        for i in range(1, 6):
            my_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            my_socket.connect(('localhost', 8000))
            #my_socket.sendto('hello from client: '.encode() + str(i).encode(), ('localhost', 8000))
            ip = 0
            if i == 1:
                ip = "10.0.1.1"
                neighborhood = [3]
            if i == 2:
                ip = "10.0.3.1"
                neighborhood = [3]
            if i == 3:
                ip = "0.0.0.0"
                neighborhood = [1, 2, 4, 5]
            if i == 4:
                ip = "10.0.2.1"
                neighborhood = [3, 5]
            if i == 5:
                ip = "10.0.4.1"
                neighborhood = [3, 4]

            router = Router(i, ip, '255.255.255.0', neighborhood, my_socket)
            routers.append(router)

        global connections
        connections = {'r1-s1':'10.0.1.1', 'r2-s2':'10.0.3.1',
                       'r4-s4': '10.0.2.1', 'r5-s5': '10.0.4.1',
                       'r1-r3':'192.168.0.1', 'r2-r3':'192.168.0.12',
                       'r3-r1':'192.168.0.2', 'r3-r2':'192.168.0.18',
                       'r3-r4':'192.168.0.5', 'r3-r5':'192.168.0.13',
                       'r4-r3':'192.168.0.6', 'r4-r5':'192.168.0.9',
                       'r5-r3':'192.168.0.14', 'r5-r4':'192.168.0.10'}

        global listaRouters
        listaRouters = routers
        #print(listaRouters[0].getID())
        #listaRouters[0].printRoutingTable()

        listaRouters[0].addSubNet(0)
        listaRouters[1].addSubNet(1)
        listaRouters[2].addSubNet(2)
        listaRouters[3].addSubNet(3)
        listaRouters[4].addSubNet(4)
        #listaRouters[0].printRoutingTable()

        iter = 0
        while True:
            #R1
            self.rip(listaRouters[0], listaRouters[2])
            #print(listaRouters[2].getRouterTable())
            #time.sleep(10)

            #R2
            self.rip(listaRouters[1], listaRouters[2])
            #time.sleep(10)
            #R3
            self.rip(listaRouters[2], listaRouters[0])
            #time.sleep(10)
            self.rip(listaRouters[2], listaRouters[1])
            #time.sleep(10)
            self.rip(listaRouters[2], listaRouters[3])
            #time.sleep(10)
            self.rip(listaRouters[2], listaRouters[4])
            #time.sleep(10)

            #R4
            self.rip(listaRouters[3], listaRouters[2])
            #time.sleep(10)
            self.rip(listaRouters[3], listaRouters[4])
            #time.sleep(10)

            #R5
            self.rip(listaRouters[4], listaRouters[2])
            #time.sleep(10)
            self.rip(listaRouters[4], listaRouters[3])
            #time.sleep(10)

            try:
                for i in range(5):
                    listaRouters[i].printAndSetRoutingTable()
            except:
                pass

            print('--------------------------------------------------------------------------------------------------')
            iter += 1
            if (iter == 6):
                print("Router 3 is out")
                listaRouters[2].setStatus(0)

            time.sleep(2)







            #time.sleep(10)

        print('FINAL ROUTING TABLES')
        for i in range(5):
            listaRouters[i].printAndSetRoutingTable()



    def rip(self, r1, r2):
        global listaRouters
        if r2.up == 0:
            r1.dest_network[r2.getID() - 1] = "unreacheable"
            r1.next_hop[r2.getID() - 1] = "unreacheable"
            r1.num_hops[r2.getID() - 1] = 16
            for r in range(5):
                try:
                    if listaRouters[r].getNeighborhood().index(r):
                        listaRouters[r].dest_network[r2.getID()-1] = "unreacheable"
                        listaRouters[r].next_hop[r2.getID()-1] = "unreacheable"
                        listaRouters[r].num_hops[r2.getID()-1] = 16
                except:
                    pass

        elif r1.up == 0:
            r2.dest_network[r1.getID() - 1] = "unreacheable"
            r2.next_hop[r1.getID() - 1] = "unreacheable"
            r2.num_hops[r1.getID() - 1] = 16
            for r in range(5):
                try:
                    if listaRouters[r].getNeighborhood().index(r):
                        listaRouters[r].dest_network[r1.getID()-1] = "unreacheable"
                        listaRouters[r].next_hop[r1.getID()-1] = "unreacheable"
                        listaRouters[r].num_hops[r1.getID()-1] = 16
                except:
                    pass
        else:
            global connections
            for i in range(5):
               if(r1.dest_network[i] != 2):
                    if(r2.dest_network[i] > r1.dest_network[i] or r2.dest_network[i] == 16 ):
                        if(listaRouters[2].up != 0):
                            r2.dest_network[i] = r1.dest_network[i]+1
                            addr = ""
                            if(listaRouters[r1.getID()-1].up == 1):
                                r2.next_hop[i] = str(r1.getID())
                                r2.num_hops[i] = r1.dest_network[i]+1
                                if 0 == r2.next_hop[i]:
                                    addr = "r" + str(r2.id) + '-' + "s" + str(r2.id)
                                else:
                                    addr = "r" + str(r2.id) + '-' + "r" + str(r2.next_hop[i])
                            else:
                                r2.next_hop[i] = "unreacheable"
                                r2.num_hops[i] = 16
                                addr = "unreacheable"

            r2.printAndSetRoutingTable()
            r2.getSocket().sendto(str(r2.getRouterTable()).encode() + ', src:'.encode() + str(r1.getID()).encode() + ', dest:'.encode() + str(
                    r2.getID()).encode(), ('localhost', 8000))

            # buffer size 1024
            response = r2.getSocket().recvfrom(1024)
            #print("response: ", response)
            for r in range(5):
                try:
                    #print(r)
                    if r != r1.getID()-1:
                        listaRouters[r].getNeighborhood().index(r2.getID()) #if is a neighbour
                        listaRouters[r].table[r1.getID()] = r2.table[r1.getID()]
                        #print(r, listaRouters[r].getRouterTable()[r1.getID()])

                except:
                    pass
                    #print("no")



class Router():
    def __init__(self, i, newIp, mas, neighbour, sock):
        self.id = i
        self.ip = newIp
        self.mask = mas
        self.neighborhood = neighbour
        self.my_socket = sock
        self.dest_network = [16] * 5
        self.next_hop = [16] * 5
        self.num_hops = [16] * 5
        self.table = [[0 for x in range(5)] for y in range(5)]
        self.up = 1 #up == 1, down == 0

    def getInfo(self):
        return [self.id, self.ip, self.mask, self.neighborhood, self.my_socket]

    def getNeighborhood(self):
        return self.neighborhood

    def setNeighborhood(self, newNeighborhood):
        self.neighborhood = newNeighborhood

    def getID(self):
        return self.id

    def getSocket(self):
        return self.my_socket

    def getRouterTable(self):
        return self.table

    def printAndSetRoutingTable(self):
        print('Routing table of R' + str(self.id))
        print('Destination | Next hop | address | Number of hops')

        my_table2 = ""
        global listSubredes, connections
        for i in range(5):
            addr = ""
            if 0 == self.next_hop[i]:
                addr = "r"+str(self.id)+'-'+"s"+str(self.id)
            else:
                addr = "r"+str(self.id)+'-'+"r"+str(self.next_hop[i])

            #self.table = [listSubredes[str(i+1)].ipAddress, self.next_hop[i], connections.get(addr),self.num_hops[i]]

            my_table2 = my_table2 + str(listSubredes[str(i+1)].ipAddress) + ", " + str(self.next_hop[i])+ ", "  + str(connections.get(addr))+ ", "  + str(self.num_hops[i])+ '\n'
        #print(my_table2)
            #print(listSubredes[str(i+1)].ipAddress, '   |    ', self.next_hop[i],  '   |',  connections.get(addr), ' |', self.num_hops[i])

        temp = my_table2.split('\n')
        for i in range(5):
            self.table[i] = temp[i]

        for i in range(5):
            print(self.table[i])

    def addSubNet(self, i):
        self.dest_network.insert(i, 0)
        self.next_hop.insert(i, 0)
        self.num_hops.insert(i, 0)

    def setStatus(self, status):
        self.up = status




if __name__ == "__main__":
    #global listaRouters
    client = Client()
    client.main()
    #print(listaRouters)
