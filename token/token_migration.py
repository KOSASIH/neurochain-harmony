import os
import json
from web3 import Web3, HTTPProvider
from solc import compile_source

# Set up Web3 provider
w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"))

# Set up contract compilation
contract_source = open("token_contract.sol", "r").read()
compiled_contract = compile_source(contract_source, "NeuroChainToken")

# Set up contract deployment
contract_interface = compiled_contract["<stdin>:NeuroChainToken"]
bytecode = contract_interface["bin"]
abi = contract_interface["abi"]

# Deploy the contract
tx_hash = w3.eth.contract(abi=abi, bytecode=bytecode).constructor().transact({"from": "0xYOUR_DEPLOYER_ADDRESS"})

# Wait for the transaction to be mined
w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract address
contract_address = w3.eth.getTransactionReceipt(tx_hash)["contractAddress"]

# Print the contract address
print("Contract address:", contract_address)

# Save the contract address to a file
with open("contract_address.txt", "w") as f:
    f.write(contract_address)
