import phe as paillier
import json

def setup_election():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def cast_vote(vote, public_key):
    # voter machine
    if not isinstance(vote, dict):
        print("Vote is invalid")

    str = ""
    for i in vote.keys():
        str += vote[i] + "|"

    encrypted_vote = public_key.encrypt(int.from_bytes(str.encode('ascii'), byteorder='big'))

    payload = {
        "ciphertext": encrypted_vote.ciphertext(),
        "exponent": encrypted_vote.exponent
    }
    return json.dumps(payload)

class Ballot_Server:
    def __init__(self, public_key):
        self.public_key = public_key
        self.encrypted_ballots = []
        self.ballot_count = 0

    def recieve_vote(self, payload_json):
        payload = json.loads(payload_json)

        encrypted_vote = paillier.paillier.EncryptedNumber(
            self.public_key,
            int(payload["ciphertext"]),
            int(payload["exponent"])
        )
        self.encrypted_ballots.append(encrypted_vote)
        self.ballot_count += 1
        print(f"    Ballot {self.ballot_count:02d} received | "
              f"ciphertext={str(encrypted_vote.ciphertext())[:30]}...")


    def get_encrypted_tally(self):
        """
        Homomorphically sum all ballots.
        Returns a single encrypted value = Enc(total votes for B).
        No plaintext is ever touched.
        """
        if not self.encrypted_ballots:
            raise ValueError("No ballots received")
        return sum(self.encrypted_ballots)

def decrypt_final_tally(encrypted_tally, private_key, total_ballots):
    total_B = private_key.decrypt(encrypted_tally)
    total_A = total_ballots - total_B
    return total_A, total_B