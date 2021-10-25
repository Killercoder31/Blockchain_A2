import socket


class Node():

    # each node has a password which is later matched during verification of transactions. 
    # This simple procedure helps to keep the system tamper-free and consistent.
    def __init__(self,password, index):
        self.s=socket.socket()
        self.password = password
        self.index = index
        self.type = 1

    # type refers to which type of node it is, 0 represents as validator and 
    # 1 represents as full node
    
    def connect_to_node(self,host,port):
        self.s.connect((host,port))

    def close_conn(self):
        self.s.close()
    
    def get_verified(self,new_tran):
        if self.type == 0:
            unver_tran=str(new_tran)+self.password
            self.s.send(unver_tran.encode())
            return self.s.recv(1024).decode()
        else:
            unver_tran=str(new_tran)+self.password
            self.s.send(unver_tran.encode())
            return self.s.recv(1024).decode()


