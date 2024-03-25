import random
import logging

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

class Node:
    """
    Represents a participant in the network with a name and a reputation score.
    """
    def __init__(self, name, reputation):
        """
        Initialize a Node instance.
        
        Parameters:
            name (str): The name of the node.
            reputation (int): The reputation score of the node.
        """
        self.name = name
        self.reputation = reputation

class ProofOfStake:
    """
    Implements the Proof of Stake (PoS) consensus algorithm.
    """
    def __init__(self, nodes):
        """
        Initialize a ProofOfStake instance.
        
        Parameters:
            nodes (list): A list of Node instances representing the network participants.
        """
        self.nodes = nodes

    def select_node(self):
        """
        Selects a node to validate a block based on its reputation score.
        
        Returns:
            Node: The selected node.
        """
        total_reputation = sum(node.reputation for node in self.nodes)
        selection_point = random.uniform(0, total_reputation)
        cumulative_reputation = 0

        for node in self.nodes:
            cumulative_reputation += node.reputation
            if cumulative_reputation >= selection_point:
                return node

    def run_consensus(self, num_blocks):
        """
        Runs the consensus algorithm to validate a specified number of blocks.
        
        Parameters:
            num_blocks (int): The number of blocks to validate.
        """
        for i in range(num_blocks):
            selected_node = self.select_node()
            logging.info(f"Block {i+1} validated by node: {selected_node.name}")

def validate_input(nodes, num_blocks):
    """
    Validates input parameters.
    
    Parameters:
        nodes (list): A list of Node instances representing the network participants.
        num_blocks (int): The number of blocks to validate.
    """
    if not isinstance(nodes, list) or not all(isinstance(node, Node) for node in nodes):
        raise ValueError("Nodes should be provided as a list of Node instances.")
    if not isinstance(num_blocks, int) or num_blocks <= 0:
        raise ValueError("Number of blocks should be a positive integer.")

def run_simulation():
    """
    Runs a simulation of the Proof of Stake consensus algorithm.
    """
    nodes = [
        Node("Node A", 20),
        Node("Node B", 30),
        Node("Node C", 50)
    ]
    num_blocks = 5

    try:
        # Validate input and run simulation
        validate_input(nodes, num_blocks)
        pos = ProofOfStake(nodes)
        pos.run_consensus(num_blocks)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_simulation()
