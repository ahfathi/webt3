from hashlib import sha256
from time import time

def create_token(user):
    return sha256(('{{username: {}, password: {}, time: {}}}'.format(user.username, user.password, time())).encode()).hexdigest()