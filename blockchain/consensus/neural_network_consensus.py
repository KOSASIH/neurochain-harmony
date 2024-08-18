import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

class NeuralNetworkConsensus:
    def __init__(self, num_nodes, num_transactions, hidden_layers=2, hidden_units=128):
        self.num_nodes = num_nodes
        self.num_transactions = num_transactions
        self.hidden_layers = hidden_layers
        self.hidden_units = hidden_units
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(self.hidden_units, activation='relu', input_shape=(self.num_transactions,)))
        for _ in range(self.hidden_layers - 1):
            model.add(Dense(self.hidden_units, activation='relu'))
            model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def train(self, transactions, labels):
        self.model.fit(transactions, labels, epochs=10, batch_size=32, verbose=0)

    def validate(self, transaction):
        prediction = self.model.predict(transaction)
        return prediction > 0.5

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def serialize(self):
        return self.model.to_json()

    def deserialize(self, json_string):
        self.model = tf.keras.models.model_from_json(json_string)

    def __str__(self):
        return f"Neural Network Consensus (Hidden Layers: {self.hidden_layers}, Hidden Units: {self.hidden_units})"

# Example usage:
if __name__ == '__main__':
    num_nodes = 10
    num_transactions = 100
    consensus = NeuralNetworkConsensus(num_nodes, num_transactions)

    # Generate some sample transactions and labels
    transactions = np.random.rand(100, 100)
    labels = np.random.randint(0, 2, size=(100,))

    # Train the model
    consensus.train(transactions, labels)

    # Validate a transaction
    transaction = np.random.rand(1, 100)
    print(consensus.validate(transaction))
