# -*- coding: utf-8 -*-

import json
from time import time
from hashlib import sha256
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import requests

class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set() #create a node network

        self.new_block(0,previous_hash=0) #create a genesis block

    def new_block(self, proof, previous_hash=None):
        '''
        Creates a new block and adds it to the chain.

        Parameters:
        :param proof: <int>
        :param previous_hash: <int>

        returns the block loaded onto the blockchain
        '''
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash
        }

        #block = self.hash(block)
        self.chain.append(block)
        self.current_transactions = [] #Clear the transactions list

        return block

    def new_transaction(self,sender,recipient,amount):
        '''
        Adds a new transaction to the transaction list

        Parameters:
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount transferred

        returns the index of the block this transaction will be on
        '''
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        self.current_transactions.append(transaction)

        return len(self.chain) + 1


    def proof_of_work(self,previous_proof):
        '''
        Uses a proof-of-work algorithm to check the block.
        A proof_of_work(PoW) is how you mine a block. You do so by solving a problem whose solution is difficult to find but easy to verify.

        The problem: Find a number p that when hashed with the previous block\’s solution a hash with 4 leading 0s is produced.
        '''

        proof = 0
        while not self.valid_proof(previous_proof,proof):
            proof += 1

        return proof

        '''
         ########An earlier test######
        x = 5
        y = 0

        # find a y value that results in x*y ending in 0
        while sha256('{}'.format(x*y).encode()).hexdigest()[-1] != "0":
            y += 1

        print('The value of y is {}\n'.format(y))

        return hash(str(x*y))
        '''

    def register_node(self,address):
        '''
        Add a new node to the list of nodes

        Each node is represented by the IP address
        Parameters: <str> address (The IP)
        Adds a node to a running set of the blockchain
        '''

        '''
        url = urlparse(address)
        node = url.netloc
        '''
        self.nodes.add(address)
        return address

    def resolve_conflicts(self):
        '''
        Uses a Concensus Algorithm to resolve conflicts between blockchains in different nodes.
        It replaces the current chain with the longest one.

        returns True if there is a longer chain than this one, False otherwise
        '''
        new_chain = None
        self_max_length = len(self.chain)

        #Make requests to every node in the current network
        for node in self.nodes:
            request = requests.get('http://{}/chain'.format(node))

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            if length > self_max_length and Blockchain.valid_blockchain(chain):
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False

    @staticmethod
    def valid_blockchain(blockchain):
        '''
        Checks to see if the given blockchain is valid.
        Param: self
        returns a boolean
        '''
        #if type(blockchain) != Blockchain:
        #    raise TypeError('This is not a blockchain!')

        for index in range(len(blockchain.chain)-1,1,-1):
            if blockchain.chain[index]['previous_hash'] != blockchain.hash(blockchain.chain[index-1]):
                return False
        return True

    @staticmethod #like static methods in Java
    def hash(block):
        '''
        Hashes a block
        '''
        # creates a String from the block that was passed in, which is already in JSON format (see the code above)
        # You want to keep a sorted string to generate consistent hashes
        block_string = json.dumps(block,sort_keys=True)
        block_string = block_string.encode() #uses the String-inherent method encode() to generate a hash

        return sha256(block_string).hexdigest() #create a hexadecmial hash of the encoded string

    @staticmethod
    def valid_proof(previous_proof,proof):
        '''
        Verifies the problem: Does hash(last_proof,proof) result in 4 leading zeroes?

        Parameters:
            <int> previous_proof: Previous proof
            <int> proof: Given proof

        Returns a boolean
        '''
        #print('Previous proof: {}'.format(previous_proof))
        #print('Current proof: {}'.format(proof))

        guess = '{}{}'.format(previous_proof,proof).encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == ('0' * 4)


    @property
    ### ??? Why do I need this?
    def last_block(self):
        '''
        returns the last block in the chain
        '''
        return self.chain[-1]

    @property
    def blockchain(self):
        '''
        returns the blockchain for testing purposes
        '''
        returned_string = ''
        for block in self.chain:
            returned_string += str(block)
        return returned_string
        #print('Returning blockchain: {}'.format(self.chain))

if __name__ == '__main__':
    # Initial test suite
    test_chain = Blockchain()

    test_chain.new_transaction("Bob","Jill",5)
    test_chain.new_transaction("Bob","Jayne",10)
    test_chain.new_transaction("Bob","Jack",15.5)

    test_chain.new_block(test_chain.proof_of_work(test_chain.last_block["proof"]),0)

    test_chain.new_transaction("Bob","Jill",5)
    test_chain.new_transaction("Bob","Jayne",10)
    test_chain.new_transaction("Bob","Jack",15.5)

    test_chain.new_block(test_chain.proof_of_work(test_chain.last_block["proof"]),0)
    print('Verifying blockchain: {}'.format(Blockchain.valid_blockchain(test_chain)))

    #print(test_chain.blockchain())
