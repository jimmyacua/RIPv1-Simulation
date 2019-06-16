import socketserver
import threading

serverAddress = ('localhost', 8000)

class Server(socketserver.DatagramRequestHandler):

    def handle(self):

        print("Recieved one request from {}".format(self.client_address[0]))

        datagram = self.rfile.readline().strip()

        print("Datagram Recieved from client is:".format(datagram))

        print(datagram)
        msg = str(datagram)
        table = msg.find(']')
        tableRoutes = msg[2: -(len(msg)-(table)-1)]
        scrAndDest = msg[table+2: - 1]
        print(tableRoutes + "|" + scrAndDest)

        # Print the name of the thread

        #print("Thread Name:{}".format(threading.current_thread().name))

        # Send a message to the client

        #self.wfile.write("Message from Server! Hello Client".encode())


    # Create a Server Instance

UDPServerObject = socketserver.ThreadingUDPServer(serverAddress, Server)

# Make the server wait forever serving connections

UDPServerObject.serve_forever()
