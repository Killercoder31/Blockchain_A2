import datetime     
import hashlib     
import json     
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urllib.parse import urlparse

import socket
import socketserver

from block import Block
from time import time

class Blockchaink():

    # initiated with an empty list of blocks and then goes on to add a genesis(starting) block to it
    def __init__(self):
        self.blocks = []
        self.set_genesis_block()
        self.creation_time = time()

    # A genesis block is set at the start of the application. In the context of our implementation it does not hold any transaction 
    # information but instead serves as a logical starting point of the ledger/logbook. It has a hash code of 256 0's.
    def set_genesis_block(self):
        data = "Dexter's Coffee Shop Logbook"
        prev_hash = '0'*64
        genesis_block = Block(data,0,time(),prev_hash)
        self.blocks.append(genesis_block)

    # function to get the hash of the latest block in the chain
    def get_last_hash(self):
        last_block = self.blocks[-1]
        last_hash = last_block.hash
        return last_hash
    
    # function to add a new block to the chain
    def add_new_block(self,data,amount,timestamp):
        prev_hash = self.get_last_hash()
        new_block = Block(data,amount,timestamp,prev_hash)
        self.blocks.append(new_block)
    
    def creation_time(self):
        return self.creation_time