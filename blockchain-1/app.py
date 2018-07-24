from blockchain import Blockchain
from flask import Flask, request, jsonify, render_template, flash
from hashlib import sha256
#cross-compatibility issues
try: #Python3
    from urllib.parse import urlparse
except ImportError: #python2
    from urlparse import urlparse

#A login system that stores people's addresses


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whomst gonn guess this?'
chain = Blockchain()

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(chain.current_transactions), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction_request():
    #return jsonify(values), 201
    keymap = {
        'sender':'',
        'recipient':'',
        'amount': None
        }
    #Check to make sure all fields are filled
    for key in keymap.keys():
        value = request.args.get(key)
        if value is None:
            return 'Missing information: {}'.format(key), 400
        keymap[key] = value

    index = chain.new_transaction(keymap['sender'], keymap['recipient'], int(keymap['amount']))

    message = {
        'response':'Created a new transaction request! Your request will be located on block {}.\n'.format(index)
    }
    return jsonify(message), 201


@app.route('/mine', methods=['GET'])
def mine():
    proof = chain.proof_of_work(chain.last_block['proof']) #obtain proof of work
    flash('Mining block...')

    recipient = sha256(request.remote_addr).hexdigest() #hash ip for security purposes
    # A second line for finding ip: request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    chain.new_transaction('0',recipient,25)
    previous_hash = chain.hash(chain.last_block)

    created_block = chain.new_block(proof,previous_hash=previous_hash)

    return jsonify(created_block), 200

@app.route('/chain', methods=['GET'])
def return_chain():
    if Blockchain.valid_blockchain(chain):
        request = {
            'chain': chain.chain,
            'length': len(chain.chain)
        }
        return jsonify(request), 200

@app.route('/nodes/register', methods=['POST'])
def register_new_node():
    new_node = chain.register_node(request.remote_addr)
    response = {
        'response': 'Success! Node {} has been registered on the network'.format(new_node),
        }
    return jsonify(response), 200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    response = {}
    length = len(chain.chain)
    if chain.resolve_conflicts():
        new_length = len(chain.chain)
        response['response'] = 'Conflicts resolved. Blockchain updated from size {} to size {}'.format(length,new_length)
        return jsonify(response), 201
    response['response'] = 'Blockchain is up to date!'
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
