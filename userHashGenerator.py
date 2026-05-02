import hashlib
import os
import time
username = "colelentini"
password = "password123"

salt = str(int.from_bytes(os.urandom(64)))
print("salt: " + salt)

start = time.perf_counter_ns()
print("hash: " + str(hashlib.scrypt((username + password).encode(), 
                                    salt=salt.encode(),
                                    n=16384,
                                    r=8,
                                    p=1,
                                    ).hex()))
end = time.perf_counter_ns()
scrypt_time = end - start
print(f"Time: {scrypt_time} ns")

start = time.perf_counter_ns()
print("hash: " + str(hashlib.sha256("exampleusernameandpasswordandsalt".encode()).hexdigest()))
end = time.perf_counter_ns()
sha_time = end - start
print(f"Time: {sha_time} ns")

print(f"scrypt is {scrypt_time/sha_time} times slower")