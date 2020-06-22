import socket
import os
import time
import random
import json
import sys

sys.path.insert(0, '..') # Import the files where the modules are located
from p2pnetwork.node import Node

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8300  # The port used by the server
buffer_size = 1024

TClients=[]

def checkSnode(node):
    if node.host == HOST and node.port == PORT:
        return True
    else:
        return False

def Snode(node):
    for n in node.all_nodes:
        if n.host == HOST and n.port == PORT:
            return n

def connectWAll(clients,node):
    for client in clients:
        if client['port'] != node.port:
            print("Estableciendo conexion con: "+str(client['ip'])+':'+str(client['port']))
            node.connect_with_node(client['ip'],client['port'])


def node_callback(event, main_node, connected_node, data):
    try:
        if event != 'node_request_to_stop': # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            #print('Event: {} from main node {}: connected node {}: {}'.format(event, main_node.id, connected_node.id, data))
            if event == 'node_message':
                print(data)                            
    except Exception as e:
        print(e)

node = Node(socket.gethostbyname(socket.gethostname()),PORT+random.randrange(100), node_callback)
Nickname = input("Ingrese su nombre: ") 
node.start()
node.connect_with_node(HOST, PORT)
print("host: ",node.host,":",node.port)
node.send_to_node(Snode(node),'%?FMSG&'+node.host+'&'+str(node.port)+"&"+Nickname)
while True:
    msg = input("Ingrese mensaje: \n")
    
    if msg=="!MD":
        recvNode = input("Ingrese el nombre: ")
        msg = input("Ingrese el mensaje: ")
        node.send_to_node(Snode(node),'%?DMSG&'+node.host+'&'+str(node.port)+"&"+recvNode+"&"+msg)
    else:
        node.send_to_nodes(msg)
        os.system("clear")

node.disconnect_with_node(Snode(node))
node.stop()

