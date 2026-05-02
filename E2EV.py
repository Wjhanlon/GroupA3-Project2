import hashlib
import RSA
import CLI
import Paillier
import Database
from OneWayList import OneWayList

"""
Represent the user end of the poll
"""
def start_poll():
    while(1):

        # example hash
        """
        ex_user = "john"
        ex_pass = "222-33-4444"
        
        hashobj = hashlib.sha256(ex_user.encode())
        print(hashobj.hexdigest())

        hashobj = hashlib.sha256(ex_password.encode())
        print(hashobj.hexdigest())
        """

        # authentication system
        creds = CLI.get_creds()
        if(creds != -1):
            if(Database.database.user_exists(creds["username"])):
                print("User does not exist")

            auth = creds["username"] + creds["password"]
            
            # get salt for user
            salt = Database.database.get_salt(creds["username"])
            hashed_auth = hashlib.scrypt(auth.encode(),
                                         salt=salt.encode(),
                                         n=16384,
                                         r=8,
                                         p=1,
                                         ).hex()
            
            if(hashed_auth == Database.database.get_hash(creds["username"])):
                print("User Authenticated")
                # check if user voted
                if(Database.database.user_voted(creds["username"])):
                    print("User has already voted")
                else:
                    print("User Authenticated")

                    token, token_sig = RSA.issue_token(rsa_private_key)

                    poll_results = CLI.poll()

                    # send encrypted form
                    vote_index = CLI.candidate_to_index(poll_results["candidate"])
                    encrypted_poll = accept_vote(server, vote_index, token, token_sig)


                    try:
                        receipt = encrypted_poll
                        print("Verification Value: " + Database.database.get_hash(creds["username"]))
                        hash_list.append(Database.database.get_hash(creds["username"]))
                        receipt_list.append(receipt)
                    except Exception as e:
                        print(f"Error: {e}")

                    # print user's hash and append for final poll verification
                    # append ciphertext

                    # confirm vote

                    # set user as already voted
                    Database.database.set_voted(creds["username"])

            else:
                print("Incorrect Credentials")


        # continue votes?
        option = ""
        while(option not in ["Y", "N", "n", "y"]):
            option = input("Continue Voting? Y/N: ")
        if(option in ["N", "n"]):
            break

"""
Represent the server end of the poll
    -this would be UNVIEWABLE to attackers and voters in real world
"""
# [ {username: {hash, salt, voted?}} ]


# list used for authenticating final poll
hash_list = OneWayList([])
receipt_list = OneWayList([])

# set up ballot server
pallier_public_key, pallier_private_key = Paillier.setup_election()
rsa_private_key, rsa_public_key = RSA.generate_rsa_keypair()
server = Paillier.Ballot_Server(pallier_public_key, rsa_public_key)

# wrap receive vote in function with different parameters to protect local modification of randomness r
def accept_vote(server, vote_index, token, token_sig):
    return server.receive_vote(
        Paillier.cast_vote(vote_index, pallier_public_key),
        token,
        token_sig
    )

start_poll()

server.publish_bulletin_board()

encrypted_tally = server.get_encrypted_tally()
totalA, totalB = Paillier.decrypt_final_tally(encrypted_tally, pallier_private_key, server.ballot_count)

print(f"\n Poll Concluded")
print(f"Total Ballots: {server.ballot_count}")
print(f"Votes for William Hanlon: {totalA}")
print(f"Votes for Owen Hart: {totalB}")


print("\nVoter Hash Log:")
for i, h in enumerate(hash_list):
    print(f"  [{i+1:02d}] {h}")
