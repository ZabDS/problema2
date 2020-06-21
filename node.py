import socket
import os
import sys

sys.path.insert(0, '..') # Import the files where the modules are located
from p2pnetwork.node import Node

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9101  # The port used by the server
buffer_size = 1024

def getPort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello')
        data = s.recv(1024)        
    s.close()
    return int(data.decode())

def node_callback(event, main_node, connected_node, data):
    try:
        if event != 'node_request_to_stop': # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            #print('Event: {} from main node {}: connected node {}: {}'.format(event, main_node.id, connected_node.id, data))
            if event == 'node_message':
                print(data)

    except Exception as e:
        print(e)

port = getPort()
node = Node(HOST,port, node_callback)
node.start()
node.connect_with_node('127.0.0.1', PORT-1)

Nickname = input("Ingrese su nombre: ")
while True:
    opc = int(input("Ingrese una opcion: "))
    if opc==1:
        msg = input("Ingrese un mensaje: ")
        node.send_to_nodes(Nickname+" dice: "+msg)
