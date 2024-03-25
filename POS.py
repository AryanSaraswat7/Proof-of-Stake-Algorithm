import random

class Node:
    def __init__(self, name, reputation):
        self.name = name
        self.reputation = reputation

class ProofOfStake:
    def __init__(self, nodes):
        self.nodes = nodes

    def select_node(self):
        total_reputation = sum(node.reputation for node in self.nodes)
        selection_point = random.uniform(0, total_reputation)
        cumulative_reputation = 0

        for node in self.nodes:
            cumulative_reputation += node.reputation
            if cumulative_reputation >= selection_point:
                return node

    def run_consensus(self, num_blocks):
        for i in range(num_blocks):
            selected_node = self.select_node()
            print(f"Block {i+1} validated by node: {selected_node.name}")

# Example Usage
nodes = [
    Node("Node A", 20),
    Node("Node B", 30),
    Node("Node C", 50)
]

pos = ProofOfStake(nodes)
pos.run_consensus(5)
