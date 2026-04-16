import hashlib
import RSA
import CLI
import Paillier
from OneWayList import OneWayList

"""
Represent the user end of the poll
"""
def start_poll():
    while(1):

        # example hash
        """
        ex_user = "john"
        ex_ssn = "222-33-4444"
        
        
        hashobj = hashlib.sha256(ex_user.encode())
        print(hashobj.hexdigest())

        hashobj = hashlib.sha256(ex_password.encode())
        print(hashobj.hexdigest())
        """

        # authentication system
        creds = CLI.get_creds()
        if(creds != -1):
            if(creds["username"] not in database):
                print("User does not exist")

            auth = creds["username"] + creds["ssn"]
            
            # get salt for user
            salt = database[creds["username"]]["salt"]
            hashed_auth = hashlib.sha256((auth + salt).encode()).hexdigest()
            
            if(hashed_auth == database[creds["username"]]["hash"]):
                print("User Authenticated")
                # check if user voted
                if(database[creds["username"]]["voted"] == True):
                    print("User has already voted")
                else:
                    print("User Authenticated")

                    token, token_sig = RSA.issue_token(rsa_private_key)

                    poll_results = CLI.poll()

                    # send encrypted form
                    vote_index = CLI.candidate_to_index(poll_results["candidate"])
                    encrypted_poll = Paillier.cast_vote(vote_index, pallier_public_key)


                    try:
                        receipt = server.receive_vote(encrypted_poll, token, token_sig)
                        print("Verification Value: " + database[creds["username"]]["hash"])
                        hash_list.append(database[creds["username"]]["hash"])
                        receipt_list.append(receipt)
                    except Exception as e:
                        print(f"Error: {e}")

                    # print user's hash and append for final poll verification
                    # append ciphertext

                    # confirm vote

                    # set user as already voted
                    database[creds["username"]]["voted"] = True

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
    -this would be unviewable to attackers and voters in real world
"""
# [ {username: {hash, salt, voted?}} ]
database = {"john": {"hash": "3fa84d2e2373b99bfc810db89f1df76d4edf4b8cd7dfc6c46b4542be78d98803", 
                     "salt": "Default_Salt",
                     "voted": False},
            "owen": {"hash": "d6a6bc4ceb85391c9ba4113a36a0ea49cf4a0bad53c35d5b832ab1563a22bfae",
                     "salt": "Default_Salt",
                     "voted": False},
            "colelentini": {"hash": "d3693ab114f1e4f11704083c74c83254941c4e6e38ff07dca517db35901a4c82",
                            "salt": "Default_Salt",
                            "voted": False},
        }

# list used for authenticating final poll
hash_list = OneWayList([])
receipt_list = OneWayList([])

# set up ballot server
pallier_public_key, pallier_private_key = Paillier.setup_election()
rsa_private_key, rsa_public_key = RSA.generate_rsa_keypair()
server = Paillier.Ballot_Server(pallier_public_key, rsa_public_key)

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
