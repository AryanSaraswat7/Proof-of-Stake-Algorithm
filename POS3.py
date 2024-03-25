import random
import logging
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa



logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

class Node:
    """
    Represents a participant in the network with a public/private key pair.
    """
    def __init__(self, name, private_key):
        """
        Initialize a Node instance.
        
        Parameters:
            name (str): The name of the node.
            private_key (bytes): The private key of the node.
        """
        self.name = name
        self.private_key = private_key

    def sign_data(self, data):
        """
        Signs the given data using the node's private key.
        
        Parameters:
            data (bytes): The data to be signed.
        
        Returns:
            bytes: The signature of the data.
        """
        private_key = serialization.load_pem_private_key(
            self.private_key,
            password=None,
            backend=default_backend()
        )
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature


def generate_private_key():
    """
    Generates a private key for a node.
    
    Returns:
        bytes: The generated private key.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key_bytes

def run_simulation():
    """
    Runs a simulation as described in the scenario.
    """
    # Generate private keys for each node
    private_keys = [generate_private_key() for _ in range(4)]
    
    nodes = [
        Node("Node A", private_keys[0]),
        Node("Node B", private_keys[1]),
        Node("Node C", private_keys[2]),
        Node("Node D", private_keys[3])
    ]

    mempool = ["tx1", "tx2", "tx3", "tx4", "tx5", "tx6", "tx7", "tx8"]

    for _ in range(4):
        selected_node = random.choice(nodes)
        selected_transactions = random.sample(mempool, 2)
        mempool_hash = hashlib.sha256("".join(selected_transactions).encode()).digest()
        signature = selected_node.sign_data(mempool_hash)
        print(f"{selected_node.name} signature: {signature.hex()}")
        print()

if __name__ == "__main__":
    run_simulation()
