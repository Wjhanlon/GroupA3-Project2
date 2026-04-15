from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def sign_token(token_id: str, private_key) -> str:
    sig = private_key.sign(token_id.encode(), padding.PKCS1v15(), hashes.SHA256())
    return sig.hex()


def verify_token(token_id: str, signature_hex: str, public_key) -> bool:
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            token_id.encode(),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
