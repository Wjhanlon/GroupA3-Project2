import hashlib

import phe as paillier
import json

import RSA


def setup_election():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def cast_vote(vote, public_key):
    # voter machine

    '''
    if not isinstance(vote, dict):
        print("Vote is invalid")

    str = ""
    for i in vote.keys():
        str += vote[i] + "|"

    encrypted_vote = public_key.encrypt(int.from_bytes(str.encode('ascii'), byteorder='big'))
    '''
    encrypted_vote = public_key.encrypt(vote)
    payload = {
        "ciphertext": encrypted_vote.ciphertext(),
        "exponent": encrypted_vote.exponent
    }
    return json.dumps(payload)

class Ballot_Server:
    def __init__(self, public_key, rsa_public_key):
        self.public_key = public_key
        self.rsa_public_key = rsa_public_key
        self.encrypted_ballots = []
        self.used_tokens = set()
        self.bulletin_board = []
        self.ballot_count = 0

    def receive_vote(self, payload_json, token, token_sig):
        if not RSA.verify_token(token, token_sig, self.rsa_public_key):
            raise ValueError("Invalid token - ballot rejected")

        token_hex = token.hex()
        if token_hex in self.used_tokens:
            raise ValueError("Token already used - ballot rejected")

        self.used_tokens.add(token_hex)


        payload = json.loads(payload_json)
        encrypted_vote = paillier.paillier.EncryptedNumber(
            self.public_key,
            int(payload["ciphertext"]),
            int(payload["exponent"])
        )
        self.encrypted_ballots.append(encrypted_vote)
        self.ballot_count += 1

        receipt = hashlib.sha256(str(payload["ciphertext"]).encode()).hexdigest()
        self.bulletin_board.append(receipt)

        print(f"    Ballot {self.ballot_count:02d} received.")
        return receipt


    def get_encrypted_tally(self):
        """
        Homomorphically sum all ballots.
        Returns a single encrypted value = Enc(total votes for B).
        No plaintext is ever touched.
        """
        if not self.encrypted_ballots:
            raise ValueError("No ballots received")
        return sum(self.encrypted_ballots)

    def publish_bulletin_board(self):
        print("\n Public List of Encrypted Ballots:")
        for(i, receipt) in enumerate(self.bulletin_board):
            print(f"[{i + 1:02d}] {receipt}")

def decrypt_final_tally(encrypted_tally, private_key, total_ballots):
    total_B = private_key.decrypt(encrypted_tally)
    total_A = total_ballots - total_B
    return total_A, total_B