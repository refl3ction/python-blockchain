import time


class Block:
    def __init__(self, index, previous_hash, transactions, proof,
                 timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time.time() if timestamp is None else timestamp

    def __repr__(self):
        return """Index: {0}, Previous Hash: {1}, Proof: {2}, Transactions: {3}
        """.format(self.index, self.previous_hash,
                   self.proof, self.transactions)
