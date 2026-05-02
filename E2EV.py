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
        ex_pass = "222-33-4444"
        
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

            auth = creds["username"] + creds["password"]
            
            # get salt for user
            salt = database[creds["username"]]["salt"]
            hashed_auth = hashlib.scrypt((auth).encode(), 
                                    salt=salt.encode(),
                                    n=16384,
                                    r=8,
                                    p=1,
                                    ).hex()
            
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
    -this would be UNVIEWABLE to attackers and voters in real world
"""
# [ {username: {hash, salt, voted?}} ]
database = {"john": {"hash": "613438204179c6daa43d04e32fc0509d76b87efad1bc70f84038a1065fcdb7dec3683872c35f5d20c251248db157cb9fdea16d99753476db87ca3d9db7fd6cc9", 
                     "salt": "5491042904581601128657979932589155499693898775280553248067569895156099593707840853134279929504198257407120492966788420727587998551497525552117164422822341",
                     "voted": False},
            "owen": {"hash": "1cd6456f869982462b4d111f8abfb5c9c09e7a5a34c84b12c80ae5bab4514a4b367ca0f2da18401a5dcca9ae69708dafb319a0f2f3158eecaaafd157720bf76f",
                     "salt": "11470618636631188992448980835259862494560825989902152101415102057722156057653446316377871334408059259295477871909772111141208436623765633405097491079769148",
                     "voted": False},
            "colelentini": {"hash": "d98d585c1e65313447ed91e22ae0ac238fa66794e58de0015e971d2afae52bd473729b2fa163ee7444f2daf93260b4e01ae898bc0ddd05ab0e7deef82ac0c4f0",
                            "salt": "4474224011127718864367360795317029004273840252901266827352110545395019104677140338547586238487906388464847154944094665793056033201216940692650853568233924",
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
