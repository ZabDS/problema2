import sys
import time
import socket
import threading
sys.path.insert(0, '..') # Import the files where the modules are located
from p2pnetwork.node import Node

HOST = "localhost"
PORT = 9100

global clients

clients={}

def node_callback(event, main_node, connected_node, data):
    try:
        if event != 'node_request_to_stop': # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            print('Event: {} from main node {}: connected node {}: {}'.format(event, main_node.id, connected_node.id, data))
            if event == 'node_message':
                main_node.send_to_nodes(data)
    except Exception as e:
        print(e)

def rcvNode(Node):
    serveraddr=(HOST,PORT+1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(serveraddr)
        TCPServerSocket.listen(5)
        try:
             while True:
                Client_conn, Client_addr = TCPServerSocket.accept()
                with Client_conn:
                    data = Client_conn.recv(1024)
                    print("Recibiendo nodo, mandando información necesaria para conexión")
                    msg = str(PORT+len(Node.all_nodes)+2)
                    Client_conn.sendall(msg.encode())
        except Exception as e:
            print (e)        


print("First node")


node_1 = Node(HOST, PORT, node_callback)
node_1.start()

rcvNodes = threading.Thread(target=rcvNode,args=(node_1,), name='ServirFE')
rcvNodes.start()

#node_1.stop()
rcvNodes.join()



print('end')

