import hashlib
import RSA
import CLI
import Paillier

"""
Represent the user end of the poll
"""
def start_poll():
    while(1):

        # authentication system
        creds = CLI.get_creds()
        if(creds != -1):
            auth = creds["username"] + creds["ssn"]
            
            # get salt for user
            salt = database[creds["username"]]["salt"]
            hashed_auth = hashlib.sha256((auth + salt).encode()).hexdigest()
            print(hashed_auth)
            
            if(hashed_auth == database[creds["username"]]["hash"]):
                print("User Authenticated")
                # check if user voted
                if(database[creds["username"]]["voted"] == True):
                    print("User has already voted")
                else:
                    poll_results = CLI.poll()

                    # send encrypted form
                    encrypted_poll = Paillier.cast_vote(poll_results, pallier_public_key)
                    server.recieve_vote(encrypted_poll)

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
            "owen": {}
        }

# set up ballot server
pallier_public_key, pallier_private_key = Paillier.setup_election()
rsa_public_key, rsa_private_key = RSA.generate_rsa_keypair()
server = Paillier.Ballot_Server(pallier_public_key)

start_poll()

poll_hash = server.get_encrypted_tally()
totalA, totalB = Paillier.decrypt_final_tally(poll_hash, pallier_private_key, server.ballot_count)

print("Poll Concluded")
print(server.ballot_count)
print(totalA)
print(totalB)
print(int(totalB).to_bytes((totalB.bit_length() + 7) // 8, 'big').decode('ascii'))
