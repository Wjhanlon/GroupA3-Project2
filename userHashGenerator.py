import hashlib
username = "colelentini"
ssn = "987654321"
salt = "Default_Salt"
print(hashlib.sha256((username + ssn + salt).encode()).hexdigest())