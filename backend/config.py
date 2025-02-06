import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Connect to Ethereum Network
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load Smart Contract ABI
import json
with open("FileSignature.json", "r") as file:
    contract_abi = json.load(file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)