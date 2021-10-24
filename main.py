import sys
import random

from blockchain import Blockchain
from time import time
from transaction import Transaction
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

leader = 0

def ConnectNodes():
    global node_list, node_connection_status, connection_failed

    for ind,_node in enumerate(node_list):
        count = 0
        if node_connection_status[_node] == 0:
            try:
                node_list[ind].connect_to_node(host, port+ind)
            except:
                count += 1
        if count > len(node_list)//2:
            connection_failed = 1

def closeall():
    global node_list, node_connection_status, connection_failed

    for ind,_node in enumerate(node_list):
        node_list[ind].close_conn()

def elect_leader():
    global leader
    
    node_list[leader].type = 1
    leader = random.randint(0,len(node_list)-1)
    node_list[leader].type = 0

def proof_of_athority(new_tran):
    global node_list, node_connection_status, connection_failed, leader

    status = node_list[leader].get_verified(new_tran)

    if status == 'Verified':
        verified_by_leader.append(new_tran)
        unverified.remove(new_tran)
    confirm = True
    
    for ind, _ in enumerate(node_list):
        if ind == leader:
            continue
        else:
            status = node_list[ind].get_verified

        if status == "Malicious":
            confirm = False
    
    if confirm:
        verified.append(new_tran)
        verified_by_leader.remove(new_tran)
    else:
        verified_by_leader.remove(new_tran)
        elect_leader()

        # penalty to the leader


while(True):

    t1 = time()
    t2 = bcn.creation_time()

    # leader changes in every 3 minutes
    if abs(t1-t2) > 60*3: 
        elect_leader()


    print("Please select an option: ")
    print("1: Add a new transaction to the logbook\n" 
            + "2: View blockchain\n" 
            + "3: Admin controls\n"
            + "4: Exit")
    choice = int(input("Select: "))
    print("\n\n")

    if choice == 1:
        data = input("Please enter transaction data: ")
        amount = input("Please enter amount: ")
        print("\n\n\n")
        new_tran = Transaction(data,amount,time())
        unverified.append(new_tran)
        
        ConnectNodes()
        
        if connection_failed == 0:
            proof_of_athority(new_tran.to_string)

    elif choice == 2:
        for block in bcn.blocks:
            print()
            print(block.to_string())
        
    elif choice == 3:
        password = input("Please enter admin password('1234'):\t")
        print()
        if password != '1234':
            print("Incorrect password")
            continue

        print("Please select an option: ")
        print("1: View unverified transactions\n"+
                "2: View verified transactions\n"+
                "3: view leader nodes\n")
        admin_choice = int(input("Select: "))
        print("\n\n\n")

        if admin_choice == 1:
            if len(unverified) == 0:
                print("No unverified transactions")
                continue
            for transactions in unverified:
                print("{0}\t{1}\t{2}\t{3}".format(unverified.index(transactions),
                        transactions.data,transactions.amount,transactions.timestamp))

            print("Please choose an option: ")
            print("1: Send all for verification (Please ensure all nodes are online)\t"
                    + "2: Remove transaction from list\t"
                    + "3: Verify all\t"
                    + "4: Return")
            unverified_choice = int(input("Select: "))
            print("\n\n\n")

            if unverified_choice == 1:
                ConnectNodes()
        
                if connection_failed == 0:
                    proof_of_athority(new_tran.to_string)
                else:
                    print("Please ensure all nodes are active")
                    continue
            
            elif unverified_choice == 2:
                tran_index = input("Enter index of transaction")
                if int(tran_index) < len(unverified):
                    unverified.remove(unverified[int(tran_index)])
                else:
                    print("Invalid index")
                    continue
            
            elif unverified_choice == 3:
                for transactions in unverified:
                    verified.append(transactions)
                unverified.clear()

            else:
                continue
        
        elif admin_choice == 2:
            if len(verified) == 0:
                print("No verified transactions")
                continue
            for transactions in verified:
                print("{0}\t{1}\t{2}\t{3}".format(unverified.index(transactions),
                        transactions.data,transactions.amount,transactions.timestamp))

            print("Please choose an option: ")
            print("1: Add all to blockchain\t"
                + "2: Remove transaction from list\t"
                + "3: Return")
            verified_choice = int(input("Select: "))
            print("\n\n\n")

            if verified_choice == 1:
                for tran in verified:
                    bcn.add_new_block(tran.data,tran.amount,tran.timestamp)
                verified.clear()
            
            elif verified_choice == 2:
                tran_index = input("Enter index of transaction")
                if int(tran_index) < len(verified):
                    verified.remove(verified[int(tran_index)])
                else:
                    print("Invalid index")
                    continue

            # to return and cases of invalid input
            else: 
                continue

        elif admin_choice == 3:
            print(node_list[leader].password)    
        
        else:
            continue

    elif choice == 4:
        closeall()
        sys.exit(0)
    
    else:
        print("Could not understand the command, Please try again!")
        continue


