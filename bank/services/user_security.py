import hashlib
from bank.database.db_operations import *

def hashedPassword(salt, password):
    password = str(salt) + password

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password