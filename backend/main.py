from fastapi import FastAPI, File, UploadFile
from utils import generate_hash, digital_signature
from fastapi import FastAPI, UploadFile, Form
import hashlib
from config import w3, contract, PRIVATE_KEY
from eth_account.messages import encode_defunct
import os
from eth_account import Account
from fastapi.middleware.cors import CORSMiddleware
from web3.exceptions import ContractLogicError, Web3Exception
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/upload-file/")
async def upload_file(file: UploadFile ):
    # Read file and generate hash 
    wallet_private_key = os.getenv("PRIVATE_KEY")
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    file_hash_bytes32 = bytes.fromhex(file_hash)
    message = encode_defunct(text=file_hash)
    signed_message = w3.eth.account.sign_message(message, private_key=wallet_private_key)

    wallet_address = w3.eth.account.from_key(wallet_private_key).address
    current_nonce = w3.eth.get_transaction_count(wallet_address, 'pending')
    try:
        txn = contract.functions.signFile(file_hash_bytes32, signed_message.signature).build_transaction({
            'from': wallet_address,
            'gas': contract.functions.signFile(file_hash_bytes32, signed_message.signature).estimate_gas({'from': wallet_address}),
            'gasPrice': w3.eth.gas_price,
            'nonce': current_nonce
        })
        signed_txn = w3.eth.account.sign_transaction(txn, wallet_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return {"tx_hash": w3.to_hex(tx_hash),"result":True }
    except ContractLogicError as e:
        if "File already signed by this user" in str(e):
            return {"tx_hash": "The file has already been signed.","result":False}
        else:
            return {"tx_hash": "An error occurred: " + str(e),"result":False}
    except Web3Exception as e:
        if 'insufficient funds' in str(e):
            print(str(e))
            return {"tx_hash": "Insufficient funds for gas.","result":False}
        else:
            return {"tx_hash": "An unexpected error occurred: " + str(e),"result":False}

@app.post("/verify-signature/")
async def verify_signature(file: UploadFile):
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    file_hash_bytes32 = bytes.fromhex(file_hash)
    wallet_private_key = os.getenv("PRIVATE_KEY")
    wallet_address = w3.eth.account.from_key(wallet_private_key).address
    try:
        signer, signature, timestamp = contract.functions.verifyFile(file_hash_bytes32, wallet_address).call()
        message = encode_defunct(text=file_hash)
        recovered_address = Account.recover_message(message, signature=signature)

        # Log the signer, signature, and timestamp
        print(f"Signer: {signer}, Signature: {signature.hex()}, Timestamp: {timestamp}")

        if recovered_address.lower() == signer.lower():
            return {"signer": signer, "signature": signature.hex(), "timestamp": timestamp, "verified": True}
        else:
            return {"error": "Signature verification failed", "verified": False}
    except ContractLogicError as e:
        print(f"Contract logic error: {str(e)}")
        return {"error": "Contract logic error", "verified": False}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": "An unexpected error occurred", "verified": False}