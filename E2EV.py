import hashlib
import RSA
import CLI
import io


"""
Represent the user end of the poll
"""
def start_poll():
    while(1):

        # example hash
        """
        ex_user = "johnperveiler"
        ex_password = "potofgold"

        hashobj = hashlib.sha256(ex_user.encode())
        print(hashobj.hexdigest())

        hashobj = hashlib.sha256(ex_password.encode())
        print(hashobj.hexdigest())
        """

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


                # send encrypted form
                RSA.encrypt_RSA()

                # confirm vote

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
database = {"johnperveiler": {"hash": "3fa84d2e2373b99bfc810db89f1df76d4edf4b8cd7dfc6c46b4542be78d98803", 
                     "salt": "Default_Salt",
                     "voted": False},
            "owen": {}
        }

start_poll()

total_votes = 0

print("Poll Concluded")
print(total_votes)
