import hashlib
import RSA

"""
Represent the user end of the poll
"""

ex_user = "johnuser1234"
ex_password = "password"

hashobj = hashlib.sha256(ex_user.encode())
print(hashobj.hexdigest())

hashobj = hashlib.sha256(ex_password.encode())
print(hashobj.hexdigest())

# authentication system

# send encrypted form
RSA.encrypt_RSA()


"""
Represent the server end of the poll
"""

# [username, password, voted?]
database = [["fee8ac25b0116fd5296940f119ea3f2c336e0f9256d981ce7f423b1fb877e1dd", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", False]]

total_votes = 0

print(total_votes)

