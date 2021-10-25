import hashlib


class Block():

    def __init__(self, data, amount, timestamp, previous_block_hash):
        self.data = data
        self.amount = amount
        self.nonce = 0
        self.timestamp = timestamp
        self.prev_block_hash = previous_block_hash
        self.proof_of_work()

    def is_valid_hash(self, hash):
        return hash.startswith('0'*2)

    def proof_of_work(self):
        hash = str()
        while not self.is_valid_hash(hash):
            temp = self.to_string() + str(self.nonce)
            hash = hashlib.sha256(temp.encode()).hexdigest()

    def to_string(self):
        return "{0}\t{1}\t{2}\t{3}".format(self.data, self.amount, self.timestamp, self.prev_block_hash)
