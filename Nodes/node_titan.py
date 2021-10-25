import socket 

# this program is meant to run in a seperate bash terminal before starting the logbook application 
# it works as a node for verifying transactions that take place in Dexter's coffee shop

s=socket.socket()
port=12347
s.bind(('',port))
s.listen(5)
c,addr=s.accept()

count_accepted_transactions=1

# continues to receive data from the logbook application throughout its runtime and evaluates the 
# authenticity of the transaction by ensuring that data has not been corrupted or tampered with once
# initialised by the owner/cashier. It is assumed that the data entered is true and factual only 
# data corruption and tampering are prevented by using this mechanism

while True:
    tran=c.recv(1024).decode()
    if("Titan" in tran):
        c.send('Verified'.encode())
    else:
        c.send('Malicious'.encode())
    print("Total transaction verified today: ",count_accepted_transactions)
    count_accepted_transactions+=1