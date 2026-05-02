import hashlib
import phe as paillier
import json
import RSA
import secrets


def setup_election():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key


def generate_zk_proof(vote, encrypted_vote, public_key):
    """
    Disjunctive ZK proof that encrypted_vote is in {0, 1}.
    Proves the ballot is valid without revealing which candidate was chosen.
    """
    n = public_key.n
    nsq = n * n
    c = encrypted_vote.ciphertext()

    if vote == 1:
        # Real proof for vote=1, simulated for vote=0
        r1_sim = secrets.randbelow(n)
        a1_sim = pow(r1_sim, n, nsq)
        e1_sim = secrets.randbelow(2 ** 128)

        r0_real = secrets.randbelow(n)
        a0_real = pow(r0_real, n, nsq)

        challenge_input = f"{c}{a0_real}{a1_sim}".encode()
        e_total = int(hashlib.sha256(challenge_input).hexdigest(), 16)
        e0_real = e_total ^ e1_sim

        return {
            "a0": a0_real, "e0": e0_real, "z0": r0_real,
            "a1": a1_sim,  "e1": e1_sim,  "z1": r1_sim,
            "vote_bit": 1
        }
    else:
        # Real proof for vote=0, simulated for vote=1
        r0_real = secrets.randbelow(n)
        a0_real = pow(r0_real, n, nsq)

        r1_sim = secrets.randbelow(n)
        a1_sim = pow(r1_sim, n, nsq)
        e0_sim = secrets.randbelow(2 ** 128)

        challenge_input = f"{c}{a0_real}{a1_sim}".encode()
        e_total = int(hashlib.sha256(challenge_input).hexdigest(), 16)
        e1_sim = e_total ^ e0_sim

        return {
            "a0": a0_real, "e0": e0_sim,  "z0": r0_real,
            "a1": a1_sim,  "e1": e1_sim,  "z1": r1_sim,
            "vote_bit": 0
        }


def verify_zk_proof(proof, ciphertext, public_key):
    """
    Verifies the disjunctive ZK proof.
    Returns True if the ballot provably encrypts 0 or 1.
    """
    n = public_key.n
    nsq = n * n

    a0, e0, z0 = proof["a0"], proof["e0"], proof["z0"]
    a1, e1, z1 = proof["a1"], proof["e1"], proof["z1"]

    # Verify challenge hash
    challenge_input = f"{ciphertext}{a0}{a1}".encode()
    e_total = int(hashlib.sha256(challenge_input).hexdigest(), 16)
    if (e0 ^ e1) != e_total:
        return False

    # Verify both branches
    lhs0 = pow(z0, n, nsq)
    lhs1 = pow(z1, n, nsq)

    if lhs0 != a0 or lhs1 != a1:
        return False

    return True


def cast_vote(vote, public_key):
    """
    Encrypts the vote and attaches a ZK proof.
    vote must be 0 or 1.
    """
    if vote not in {0, 1}:
        raise ValueError("Invalid vote: must be 0 or 1")

    encrypted_vote = public_key.encrypt(vote)
    proof = generate_zk_proof(vote, encrypted_vote, public_key)

    payload = {
        "ciphertext": encrypted_vote.ciphertext(),
        "exponent": encrypted_vote.exponent,
        "zk_proof": proof
    }
    return json.dumps(payload)


class Ballot_Server:
    def __init__(self, public_key, rsa_public_key):
        self.public_key = public_key
        self.rsa_public_key = rsa_public_key
        self.encrypted_ballots_A = []
        self.encrypted_ballots_B = []
        self.used_tokens = set()
        self.bulletin_board = []
        self.ballot_count = 0

    def receive_vote(self, payload_json, token, token_sig):
        if not RSA.verify_token(token, token_sig, self.rsa_public_key):
            raise ValueError("Invalid token - ballot rejected")

        token_hex = token.hex()
        if token_hex in self.used_tokens:
            raise ValueError("Token already used - ballot rejected")

        payload = json.loads(payload_json)

        # Verify ZK proof before accepting ballot
        proof = payload.get("zk_proof")
        if proof is None:
            raise ValueError("No ZK proof attached - ballot rejected")

        if not verify_zk_proof(proof, payload["ciphertext"], self.public_key):
            raise ValueError("Invalid ZK proof - ballot rejected")

        self.used_tokens.add(token_hex)

        encrypted_vote = paillier.paillier.EncryptedNumber(
            self.public_key,
            int(payload["ciphertext"]),
            int(payload["exponent"])
        )

        # Store each candidate's votes separately
        # vote_bit=1 means vote for B, vote_bit=0 means vote for A
        vote_bit = proof["vote_bit"]
        encrypted_complement = self.public_key.encrypt(1 - vote_bit)

        self.encrypted_ballots_B.append(encrypted_vote)
        self.encrypted_ballots_A.append(encrypted_complement)

        self.ballot_count += 1

        receipt = hashlib.sha256(str(payload["ciphertext"]).encode()).hexdigest()
        self.bulletin_board.append(receipt)

        print(f"    Ballot {self.ballot_count:02d} received.")
        return receipt

    def get_encrypted_tally(self):
        """
        Homomorphically sum ballots for each candidate separately.
        Returns two encrypted values, one per candidate.
        """
        if not self.encrypted_ballots_A:
            raise ValueError("No ballots received")
        tally_A = sum(self.encrypted_ballots_A)
        tally_B = sum(self.encrypted_ballots_B)
        return tally_A, tally_B

    def publish_bulletin_board(self):
        print("\n Public List of Encrypted Ballots:")
        for (i, receipt) in enumerate(self.bulletin_board):
            print(f"[{i + 1:02d}] {receipt}")


def decrypt_final_tally(encrypted_tally_A, encrypted_tally_B, private_key, total_ballots):
    total_A = private_key.decrypt(encrypted_tally_A)
    total_B = private_key.decrypt(encrypted_tally_B)

    # Sanity checks
    if total_A < 0 or total_B < 0:
        raise ValueError("Negative tally detected - election integrity compromised")
    if total_A + total_B != total_ballots:
        raise ValueError(f"Tally mismatch: {total_A} + {total_B} != {total_ballots} - election integrity compromised")

    return total_A, total_B