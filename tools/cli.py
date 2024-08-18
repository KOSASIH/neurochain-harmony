import argparse
import json
import os
import sys
from typing import List

from rich.console import Console
from rich.table import Table

from neural_network_consensus import NeuralNetworkConsensus
from contracts import DataContract, SmartContract

console = Console()

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="High-Tech CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Create a subparser for the "consensus" command
    consensus_parser = subparsers.add_parser("consensus", help="Run the neural network consensus algorithm")
    consensus_parser.add_argument("--nodes", type=int, default=3, help="Number of nodes in the network")
    consensus_parser.add_argument("--transactions", type=str, nargs="+", help="Transactions to validate")

    # Create a subparser for the "contract" command
    contract_parser = subparsers.add_parser("contract", help="Interact with a smart contract")
    contract_parser.add_argument("--address", type=str, required=True, help="Smart contract address")
    contract_parser.add_argument("--function", type=str, required=True, help="Smart contract function to call")
    contract_parser.add_argument("--args", type=str, nargs="+", help="Arguments to pass to the smart contract function")

    # Create a subparser for the "data" command
    data_parser = subparsers.add_parser("data", help="Interact with a data contract")
    data_parser.add_argument("--address", type=str, required=True, help="Data contract address")
    data_parser.add_argument("--key", type=str, required=True, help="Key to retrieve from the data contract")
    data_parser.add_argument("--value", type=str, help="Value to update the data contract with")

    return parser

def run_consensus(args: argparse.Namespace) -> None:
    nn_consensus = NeuralNetworkConsensus(args.nodes)
    transactions = [json.loads(tx) for tx in args.transactions]
    results = nn_consensus.validate(transactions)
    console.print("Consensus results:", results)

def run_contract(args: argparse.Namespace) -> None:
    smart_contract = SmartContract(args.address)
    result = smart_contract.execute_function(args.function, args.args)
    console.print("Smart contract result:", result)

def run_data(args: argparse.Namespace) -> None:
    data_contract = DataContract(args.address)
    if args.value:
        data_contract.update_data({args.key: args.value})
        console.print("Data contract updated successfully")
    else:
        value = data_contract.get_data(args.key)
        console.print("Data contract value:", value)

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "consensus":
        run_consensus(args)
    elif args.command == "contract":
        run_contract(args)
    elif args.command == "data":
        run_data(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
