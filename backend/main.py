from fastapi import FastAPI, File, UploadFile
from utils import generate_hash, digital_signature
from fastapi import FastAPI, UploadFile, Form
import hashlib
from config import w3, contract, PRIVATE_KEY
from eth_account.messages import encode_defunct
import os
from eth_account import Account

app = FastAPI()

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
    txn = contract.functions.signFile(file_hash_bytes32, signed_message.signature).build_transaction({
        'from': wallet_address,
        'gas': 2000000,
        'gasPrice': w3.to_wei('25', 'gwei'),
        'nonce': current_nonce
    })
    signed_txn = w3.eth.account.sign_transaction(txn, wallet_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return {"tx_hash": w3.to_hex(tx_hash)}

@app.post("/verify-signature/")
async def verify_signature(file: UploadFile):
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    file_hash_bytes32 = bytes.fromhex(file_hash)
    try:
        signer, signature, timestamp = contract.functions.verifyFile(file_hash_bytes32).call()
        
        # Create a message object
        message = encode_defunct(text=file_hash)
        
        # Recover the address from the signature
        recovered_address = Account.recover_message(message, signature=signature)
        
        # Verify if the recovered address matches the expected signer
        if recovered_address.lower() == signer.lower():
            return {"signer": signer, "signature": signature.hex(), "timestamp": timestamp, "verified": True}
        else:
            return {"error": "Signature verification failed", "verified": False}
    except:
        return {"error": "File not found"}