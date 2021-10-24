import datetime     
import hashlib     
import json     
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urllib.parse import urlparse

import socket
import socketserver
import sys

from blockchain import Blockchain
from time import time
# from transaction import Transaction
from node import Node


host='127.0.0.1'
port=12345


bcn = Blockchain()
unverified = []
verified_by_leader = []
verified = []

node_list = []
node_list.append(Node('Pluto', 0))
node_list.append(Node('Jupiter', 1))
node_list.append(Node('Titan', 2))


node_connection_status = {}
for _node in node_list:
    node_connection_status[_node] = 0

connection_failed = 0

def ConnectNodes():
    global node_list, node_connection_status

    for ind,_node in enumerate(node_list):
        if node_connection_status[_node] == 0:
            node_list[ind].connect_to_node(host, port+ind)



while(True):
    print("Please select an option: ")
    print("1: Add a new transaction to the logbook\n" 
            + "2: View blockchain\n" 
            + "3: Admin controls\n"
            + "4: Exit")
    choice = int(input("Select: "))
    print("\n\n")

    # the new transaction is compiled by using details given by user and computing timestamp and 
    # added to the unverified pool if all nodes are found to be online it is batched for verification 
    # else it sits in the unverified pool for superuser intervention

    if choice == 1:
        break

    elif choice == 2:
        break

    elif choice == 3:
        break

    elif choice == 4:
        sys.exit()
    
    else:
        print("Could not understand the command, Please try again!")
        continue


