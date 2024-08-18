{
  "node_id": "node-1",
  "node_type": "data_provider",
  "data_contract_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "data_id": "weather_data",
  "data_update_interval": 300, // 5 minutes
  "data_update_url": "https://api.openweathermap.org/data/2.5/weather",
  "data_update_params": {
    "q": "London,UK",
    "units": "metric",
    "appid": "YOUR_API_KEY"
  },
  "node_private_key": "0x1234567890abcdef",
  "node_public_key": "0x9876543210fedcba",
  "node_encryption_key": "0x1234567890abcdef",
  "node_decryption_key": "0x9876543210fedcba",
  "node_neural_network_model": "models/weather_model.h5",
  "node_neural_network_weights": "models/weather_weights.h5",
  "node_quantum_resistant_cryptography": true,
  "node_consensus_algorithm": "neural_network_consensus",
  "node_consensus_threshold": 0.5,
  "node_network_id": "network-1",
  "node_network_nodes": [
    "node-2",
    "node-3",
    "node-4"
  ]
}
