import unittest
import numpy as np
from neural_network_consensus import NeuralNetworkConsensus

class TestNeuralNetworkConsensus(unittest.TestCase):
    def setUp(self):
        self.nn_consensus = NeuralNetworkConsensus(3)  # 3 nodes in the network

    def test_validate_transaction(self):
        # Create a sample transaction
        transaction = {
            "sender": "node-1",
            "receiver": "node-2",
            "amount": 10.0,
            "data": "some data"
        }

        # Create a sample neural network output
        nn_output = np.array([0.9, 0.1, 0.0])  # node-1 is the most trusted node

        # Validate the transaction using the neural network consensus algorithm
        result = self.nn_consensus.validate(transaction, nn_output)

        self.assertTrue(result)  # The transaction should be valid

    def test_validate_block(self):
        # Create a sample block
        block = {
            "block_number": 1,
            "transactions": [
                {"sender": "node-1", "receiver": "node-2", "amount": 10.0, "data": "some data"},
                {"sender": "node-2", "receiver": "node-3", "amount": 20.0, "data": "some other data"}
            ]
        }

        # Create a sample neural network output
        nn_output = np.array([0.9, 0.1, 0.0])  # node-1 is the most trusted node

        # Validate the block using the neural network consensus algorithm
        result = self.nn_consensus.validate(block, nn_output)

        self.assertTrue(result)  # The block should be valid

    def test_consensus_algorithm(self):
        # Create a sample neural network output
        nn_output = np.array([0.9, 0.1, 0.0])  # node-1 is the most trusted node

        # Run the consensus algorithm
        result = self.nn_consensus.consensus_algorithm(nn_output)

        self.assertEqual(result, "node-1")  # node-1 should be the leader

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
