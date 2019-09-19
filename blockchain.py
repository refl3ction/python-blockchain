import functools
import hashlib
import json
import util.hash_util as hash_util
import pickle
from block import Block
from transaction import Transaction
from util.verification import Verification
from wallet import Wallet

MINING_REWARD = 10
participants = {'Denis'}


class Blockchain:

    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node_id = hosting_node_id
        self.__peer_nodes = set()
        self.load_data()

    # Cria o getter padrão ao acessar o atributo de outras classes
    @property
    def chain(self):
        return self.__chain[:]

    # Pode restringir o setter
    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):

        try:
            with open('blockchain.txt', mode='r') as f:
                # pickle
                # file_content = pickle.loads(f.read())
                # blockchain = file_content['blockchain']
                # open_transactions = file_content['open_transactions']

                file_content = f.readlines()
                print(file_content)
                tmp_blockchain = json.loads(file_content[0][:-1])
                self.chain = []
                for block in tmp_blockchain:
                    transactions = [Transaction(tx['sender'],
                                                tx['recipient'],
                                                tx['signature'],
                                                tx['amount'])
                                    for tx in block['transactions']]

                    updated_block = Block(
                        block['index'], block['previous_hash'], transactions,
                        block['proof'], block['timestamp'])

                    self.__chain.append(updated_block)

                tmp_open_transactions = json.loads(file_content[1][:-1])
                for tx in tmp_open_transactions:
                    updated_transaction = Transaction(tx['sender'],
                                                      tx['recipient'],
                                                      tx['signature'],
                                                      tx['amount'])
                    self.__open_transactions.append(updated_transaction)

                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)

        except (IOError, IndexError):
            print('Handled Exception...')
            pass
        finally:
            print('Cleanup!')

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                # data = {
                #     'blockchain': blockchain,
                #     'open_transactions': open_transactions
                # }
                # f.write(pickle.dumps(data))
                saveble_chain = [
                    block.__dict__
                    for block in [Block(block_el.index, block_el.previous_hash,
                                        [tx.__dict__
                                         for tx in block_el.transactions],
                                        block_el.proof, block_el.timestamp)
                                  for block_el in self.__chain]
                ]
                f.write(json.dumps(saveble_chain))

                saveble_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write('\n')
                f.write(json.dumps(saveble_tx))

                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))

        except IOError:
            print('Could not save file.')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions,
                                           last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        if self.hosting_node_id is None:
            return None

        participant = self.hosting_node_id
        tx_sender = [
            [tx.amount
             for tx in block.transactions
             if tx.sender == participant]
            for block in self.__chain
        ]

        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions
                          if tx.sender == participant]

        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(
            lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
            if len(tx_amount) > 0
            else tx_sum + 0, tx_sender, 0
        )

        tx_recipient = [
            [tx.amount for tx in block.transactions
             if tx.recipient == participant]
            for block in self.__chain
        ]
        amount_received = functools.reduce(
            lambda tx_sum, tx_amount: tx_sum + sum(tx_amount)
            if len(tx_amount) > 0
            else tx_sum + 0, tx_recipient, 0
        )
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
        :sender: The sender of the coins
        :recipient: The recipient of the coins
        :amount: The amount of coins to send (default=1.0)
        """

        if self.hosting_node_id is None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True

        return False

    def mine_block(self):
        if self.hosting_node_id is None:
            return None

        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)

        proof = self.proof_of_work()

        # Create reward for miners
        reward_transaction = Transaction(
            'MINING', self.hosting_node_id, '', MINING_REWARD)

        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Remove a node to the peer node set.

        Arguments:
            :node: The node URL which should be added
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes.
        """
        return list(self.__peer_nodes)
