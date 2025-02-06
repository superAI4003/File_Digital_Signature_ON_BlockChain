import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives import serialization

def generate_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()

def digital_signature(file_hash):
    private_key = ec.generate_private_key(ec.SECP256R1())
    pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
    )
    print(pem.decode('utf-8'))
    signature = private_key.sign(file_hash.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()