import hashlib


def hash_password_(password):
    return hashlib.sha256(password.encode()).hexdigest()