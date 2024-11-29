import hashlib
import re
def hash_password_(password):
    return hashlib.sha256(password.encode()).hexdigest()
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None



if __name__ == '__main__':
    pasw = hash_password_('123')
    print(pasw)
