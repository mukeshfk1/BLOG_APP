
from werkzeug.security import generate_password_hash,check_password_hash


def hash_password(plain_pass):

    hash_pass = generate_password_hash(plain_pass)
    return hash_pass

def verify_password(hash_pass,plain_pass):
    match_pass = check_password_hash(hash_pass,plain_pass)

    

    return match_pass
