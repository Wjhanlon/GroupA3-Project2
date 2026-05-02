import hashlib
import os
username = "colelentini"
password = "password123"

salt = str(int.from_bytes(os.urandom(64)))
print("salt: " + salt)

print("hash: " + str(hashlib.scrypt((username + password).encode(), 
                                    salt=salt.encode(),
                                    n=16384,
                                    r=8,
                                    p=1,
                                    ).hex()))