from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import os


def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def issue_token(private_key):
    token = os.urandom(32)
    sig = private_key.sign(token, padding.PKCS1v15(), hashes.SHA256())
    return token, sig.hex()


def verify_token(token_id, signature_hex, public_key):
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            token_id,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
