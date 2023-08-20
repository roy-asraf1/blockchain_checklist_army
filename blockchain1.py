# Module 1 - Create a Blockchain

# install libarys
# pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain

# defined the class
class Blockchain:

    def __init__(self):
        self.chain = []  # the chain in the blockchain
        self.create_block(proof=1, previous_hash='0')  # first block in the blockhcain, the first

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'military_equipment': self.check_military_equipment()}
        self.chain.append(block)
        return block

    def check_military_equipment(self):
        check_input = False
        inputequipment =""
        size =0
        array = {}
        while (size !=4):

            helmet = input("Enter Y or N for helmet: ")
            if helmet == 'Y' or helmet == 'N':
                print("You entered:", helmet)
                array[0] = helmet
                size = size + 1

            bottle = input("Enter Y or N for bottle: ")
            if bottle == 'Y' or bottle == 'N':
                print("You entered:", bottle)
                array[1] = bottle
                size = size + 1

            belt = input("Enter Y or N for belt: ")
            if belt != 'Y' or belt != 'N':
                print("You entered:", belt)
                array[2] = belt
                size = size + 1

            gun = input("Enter Y or N for gun: ")
            if gun != 'Y' or gun != 'N':
                print("You entered:", gun)
                array[3] = gun
                size = size + 1

            for i in array:
                if array[i] != 'Y' or array[i] != 'N':
                    print("input Error do this again")
                    break
        return inputequipment

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            if not self.check_military_equipment():
                print("military equipment was changed")
                return False

            previous_block = block
            block_index += 1
        return True


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port=5000)
