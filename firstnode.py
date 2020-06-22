import sys
import time
import socket
import threading
import json
sys.path.insert(0, '..') # Import the files where the modules are located
from p2pnetwork.node import Node

HOST = "localhost"
PORT = 8300

global clients
clients=[]

def getNameNode(nodeID):
    for client in clients:
        if client['id']== nodeID:
            return client['name']

def sendMsgToAll(msg,nodeID,mainNode):
    for client in clients:
        if client['id'] == nodeID:
            for node in mainNode.all_nodes:
                if node.id != nodeID:
                    mainNode.send_to_node(node,client['name']+": "+msg+"\nInserte Mensaje:")
            break

def sendMsgToOne(msg,nodeName,mainNode,nameSend):
    for client in clients:
        if client['name'] == nodeName:
            for node in mainNode.all_nodes:
                if node.id == client['id']:
                    mainNode.send_to_node(node,nameSend+"(privado): "+msg+"\nInserte Mensaje:")
                    return True
    return False        
                

def node_callback(event, main_node, connected_node, data):
    try:
        if event != 'node_request_to_stop': # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            #print('Event: {} from main node {}: connected node {}: {}'.format(event, main_node.id, connected_node.id, data))
            if event == 'inbound_node_connected':
                print("Enviando tabla de clientes:")
                #main_node.send_to_nodes((json.dumps(clients)))
            elif event == 'node_message':
                aux=data.split('&')
                if(aux[0]=="%?FMSG"):
                    Daux={'ip':aux[1],'port':aux[2],'id':connected_node.id,'name':aux[3]}
                    clients.append(Daux)
                elif(aux[0]=="%?DMSG"):
                    name1=getNameNode(connected_node.id)
                    if(sendMsgToOne(aux[4],aux[3],main_node,name1)):
                        print("Mensaje privado enviado")
                else:
                    sendMsgToAll(data,connected_node.id,main_node)

    except Exception as e:
        print(e)

print("First node")


node_1 = Node(HOST, PORT, node_callback)
node_1.start()

print(node_1.name)
print('end')

