import json
import random
import string


def random_string():
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1000))
    return s

def get_credentials():
    username = input('Enter your username: ')
    password = input(f'Enter your password {username}: ')
    return username, password

def read_passwdb():
    with open('passwd.json', 'r') as pwdb_file:
        pwdb = json.load(pwdb_file)
    return pwdb

def write_passwdb(pwdb):
    with open('passwd.json', 'w') as pwdb_file:
        json.dump(pwdb, pwdb_file)

def pwhash(salt, password):
    pwh = 0
    to_hash = salt + password
    for i, char in enumerate(to_hash):
        pwh += (i + 1) * ord(char)
    return str(pwh)

def add_user(pwdb, username, password):
    if username not in pwdb:
        salt = random_string()
        hashed_pass = pwhash(salt, password)
        pwdb[username] = salt, hashed_pass

def authenticate(username, password, pwdb):
    if username in pwdb:
        salt, password = pwdb[username]
        hashed_password = pwhash(salt, password)
        if hashed_password == password:
            return True
        else:
            return False
    else:
        add_user(pwdb, username, password)
        return True

def main():
    username, password = get_credentials()
    pwdb = read_passwdb()
    status = authenticate(username, password, pwdb)
    if status:
        print('Success!')
    else:
        print('Wrong username or password!')
    write_passwdb(pwdb)

if __name__ == '__main__':
    main()
