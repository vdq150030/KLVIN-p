#TCP server for python3
import socket
import sys
import time 

import os, datetime, time, platform
from os.path import isfile, join

import multiprocessing

class TCPServer(object):
    # Server socket created, bound and starting to listen

    Server_Socket = None

    Server_IP = ''
    Server_Port = 8000
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
    server_addr = (Server_IP, Server_Port)

    event = None

    def __init__(self, IP: str,port: int, e = None, buffer_size = 1024):

        # Prepare a server socket
        self.Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket function creates a socket.

        try:
            self.__bind_socket(IP,port)
            self.Server_IP = IP
            self.Server_Port = port 
            self.BUFFER_SIZE = buffer_size
            self.event = e
            
            self.Server_Socket.listen(5)
            self.Server_Socket.settimeout(1)
            
            print("Server is listening on ", self.Server_IP, ":", self.Server_Port)
            # Listening but not accepting connection yet ?
        except Exception as e:
            raise e
            

    def __bind_socket(self,ip, port):
        print ("Attempting to bind to {}:{}".format(ip,port) )
        try:
            self.Server_Socket.bind((ip, port))
            
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg))
            raise msg
        
    def run(self):

        running = True
        while running:

            client_connection = None
            while (client_connection == None):

                print("{}:{} :: Accepting new connection...".format(self.Server_IP, self.Server_Port) ) 
                try:
                    client_connection, addr = self.Server_Socket.accept()
                except Exception as e:
                    if (e == KeyboardInterrupt):
                        break
                        
            connecting = True
            while connecting:
                print('Connection address:', addr)
                
                try:
                    command = client_connection.recv(self.BUFFER_SIZE).decode()
                except Exception as e:
                    print(e)
                    connecting = False

                print (command)
                # trim \n from some java clients
                #if (command[-1:] == '\n'):
                #    command = command[:-2] # two of them
                
                if(command == '8'):
                    # reset signal 
                    print ("Reset signal received from android.")
                    self.event.set()
                    break

                elif(command == '7'):
                    mypath = "./resources/videos"
                    # get available file in the resource/videos folder 
                    for f in os.listdir(mypath):
                        if isfile(join(mypath, f)):
                            print ("{} ".format(join(mypath, f)) )
                            client_connection.send( str("{} ".format(f) ).encode()) # java
                    break

                elif (command.split()[0] == "GET"):
                    # basically command 6 but in GET request  
                    filepath = "./resources/"+ command.split()[1].partition("/")[2]
                    print ("get request to " + filepath)
                    try:
                        sendFile = open(filepath, "rb") # could have let client known the file extension
                    except IOError:
                        print ("File not found.")
                        break

                    while True:
                        print("----transmiting that block of data----")
                        b = sendFile.read(self.BUFFER_SIZE)
                        print(b)

                        if not b:
                            #client_connection.send("\n".encode()) # java writer
                            connecting = False
                            break
                        else:
                            client_connection.send(b)
                    print("Done.")
                    sendFile.close()
                    break

                elif(command == '6'):
                    # send video file
                    print("6")
                    sendFile = open("./resources/videos/turtle.mp4", "rb") # could have let client known the file extension

                    while True:
                        print("----transmiting that block of data----")
                        b = sendFile.read(self.BUFFER_SIZE)
                        print(b)

                        if not b:
                            #client_connection.send("\n".encode()) # java writer
                            connecting = False
                            break
                        else:
                            client_connection.send(b)
                    print("Done.")
                    sendFile.close()
                    break


                elif (command == '5'):
                    # send image
                    print("5")
                    sendFile = open("./resources/images/corgi.jpg", "rb")

                    while True:
                        print("----transmiting that block of data----")
                        b = sendFile.read(self.BUFFER_SIZE)
                        print(b)

                        if not b:
                            #client_connection.send("\n".encode()) # java writer
                            connecting = False
                            break
                        else:
                            client_connection.send(b)
                    print("Done.")
                    sendFile.close()
                    break

                elif (command == '4'):
                    print("Termination signal received. Closing server.")
                    connecting = False
                    running = False
                    break

                elif (command == '3' or not command):
                    print("Connection lost.")
                    connecting = False
                    break
                    
                elif (command == '2'):
                    print("2")
                    
                    sendFile = open("./resources/data/temperature.txt", "r")

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
                    break

                elif (command == '1'):
                    # serve as a ping signal
                    client_connection.send( str("{} Howdy!\n".format(self.Server_Port) ).encode()) # java
                    break

                else:
                    client_connection.send("Invalid command\n".encode())
                        
            # could have a goodbye message here before closing
            client_connection.close()
        
        print ("Shutting down server..")
        self.Server_Socket.close()
        pass


if (__name__ == '__main__'):
    print("test run")
    tcp_server = TCPServer("localhost",8000)
    tcp_server.run()



        

    
