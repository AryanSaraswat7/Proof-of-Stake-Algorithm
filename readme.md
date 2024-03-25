# Proof of Stake (PoS) Implementation in Python

This Python script demonstrates a basic implementation of a Proof of Stake (PoS) consensus algorithm. In PoS, the probability of a node being chosen to validate transactions and create new blocks is proportional to its stake, or reputation, in the network.

## Overview

The implementation consists of two main classes:

1. **Node**: Represents a participant in the network with a name and a reputation score.
2. **ProofOfStake**: Contains the logic for selecting nodes based on their reputation to validate blocks.

## How It Works

1. **Node Class**: Defines a `Node` class with attributes for name and reputation.
2. **ProofOfStake Class**: Contains methods for selecting a node based on reputation and running the consensus algorithm.
    - `select_node()`: Randomly selects a node weighted by its reputation score.
    - `run_consensus(num_blocks)`: Simulates the validation of a specified number of blocks by selecting nodes according to the PoS algorithm.

## Usage

1. Define nodes with different reputation scores.
2. Initialize a `ProofOfStake` object with the list of nodes.
3. Run the consensus algorithm using the `run_consensus()` method.

## Example

```python
nodes = [
    Node("Node A", 20),
    Node("Node B", 30),
    Node("Node C", 50)
]

pos = ProofOfStake(nodes)
pos.run_consensus(5)
