from werkzeug.security import generate_password_hash,check_password_hash


given_pass='qwerty'

hash_pass = generate_password_hash(given_pass)

print("hash_pass : " ,hash_pass)

match_pass = check_password_hash(hash_pass,given_pass)

print(match_pass)