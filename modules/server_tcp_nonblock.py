#TCP server for python3
# TODO: proper closing method
import socket
import sys
import time 

class TCPServer(object):
    # Server socket created, bound and starting to listen

    Server_Socket = None

    Server_IP = ''
    Server_Port = 8000
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
    server_addr = (Server_IP, Server_Port)

    def __init__(self,IP: str,port: int,buffer_size = 1024):

        # Prepare a server socket
        self.Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket function creates a socket.

        if (self.__bind_socket(IP,port)):
            self.Server_IP = IP
            self.Server_Port = port 
            self.BUFFER_SIZE = buffer_size
            
            self.Server_Socket.listen(5)
            self.Server_Socket.settimeout(1)

            print("Server is listening on ", self.Server_IP, ":", self.Server_Port)
            # Listening but not accepting connection yet ?
        else:
            raise socket.error 

    def __bind_socket(self,ip, port) -> bool:
        print ("Attempting to bind to {}:{}".format(ip,port) )
        try:
            self.Server_Socket.bind((ip, port))
            #self.Server_Socket.bind(('wlan0',port))
            return True

        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg))
            return False
        
    def run(self):

        running = True
        try:
            while running:

                client_connection = None
                while (client_connection == None):

                    print("{}:{} :: Accepting new connection...".format(self.Server_IP, self.Server_Port) ) 
                    try:
                        client_connection, addr = self.Server_Socket.accept()
                    except Exception as e:
                        if (e == KeyboardInterrupt):
                            raise e

                connecting = True
                while connecting:
                    print('Connection address:', addr)

                    try:
                        command = client_connection.recv(self.BUFFER_SIZE).decode()
                    except Exception as e:
                        print(e)
                        connecting = False

                    # trim \n from picky java clients
                    if (command[-1:] == '\n'):
                        command = command[:-2] # two of them

                    if (command == '4'):
                        print("Termination signal received. Closing server.")
                        connecting = False
                        running = False
                        break

                    elif (command == '3' or not command):
                        print("Connection lost.")
                        connecting = False
                        break

                    elif (command == '5'):
                        print("5")
                        # need a serialize function
                        sendFile = open("./modules/resources/pi.jpg", "rb")

                        while True:
                            print("----transmiting that block of data----")
                            b = sendFile.read(self.BUFFER_SIZE)
                            print(b)

                            if not b:
                                #client_connection.send("\n".encode()) # java
                                connecting = False
                                break
                            else:
                                client_connection.send(b.encode())
                        print("Done.")
                        sendFile.close()                    

                    elif (command == '2'):
                        print("2")

                        sendFile = open("./log/data.txt", "r")

                        while True:
                            print("----transmiting that block of data----")
                            l = sendFile.read(self.BUFFER_SIZE)
                            print(l)

                            if not l:
                                #client_connection.send("\n".encode()) # java
                                connecting = False
                                break
                            else:
                                client_connection.send(l.encode())
                        print("Done.")
                        sendFile.close()

                    elif (command == '1'):
                        # serve as a ping signal
                        client_connection.send( str("{} Howdy!\n".format(self.Server_Port) ).encode()) # java
                        break

                    else:
                        client_connection.send("Invalid command\n".encode())

                client_connection.close()
        
        except KeyboardInterrupt or Exception as e:
            self.Exit()
            raise e 

        self.Exit()

    def Exit(self):
        print ("{} : Exit.".format(__name__))
        self.Server_Socket.close()


#tcp_server = TCPServer("192.168.1.31",8000)
#tcp_server.run()
