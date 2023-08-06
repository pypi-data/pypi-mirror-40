import os
import json
from cryptography.fernet import Fernet
from pkg_resources import resource_filename
from .encryption import Encryption
from .encryption import check_valid_fernet

from .vault import Vault as vault # to keep previous version working.

master_key_file = resource_filename(__name__, 'master_key.json')
keys_file = resource_filename(__name__, 'keys.json')

# Internal methods
def _check_master_key():
    """Verifies if there's already a master key"""
    if os.path.exists(master_key_file):
        # read master key from file and return it
        with open(master_key_file) as file_handler:
            data = json.load(file_handler)
            key = data['key']
        return key

    else: # we need a new master key
        key = Fernet.generate_key()
        key = key.decode('utf-8')
        data = {'key': key}
        with open(master_key_file, 'w') as file_handler:
            file_handler.write(json.dumps(data))
        return key

def _read_persistent_vault():
    """Returns existing data in the keys file."""
    if os.path.exists(keys_file):
        with open(keys_file) as file_handler:
            data = json.load(file_handler)
        return data
    else: # create empty
        with open(keys_file, 'w') as file_handler:
            data = {}
            file_handler.write(json.dumps(data))
        return data


def _update_persistent_vault():
    """Overwrites data in the keys file with vault's instance values."""
    with open(keys_file, 'w') as file_handler:
        file_handler.write(json.dumps(vault))


master_key = _check_master_key()
vault = _read_persistent_vault()

# Public methods
def replace_master_key(key):
    """
    Replaces master key for the vault.
    
    :param key: (str) a valid Fernet key.
                Must be 32 url-safe base64-encoded bytes
                also accepts Fernet.generate_key() as input
    """
    if check_valid_fernet(key):
        with open(master_key_file, 'w') as file_handler:
            if type(key) == bytes:
                key = key.decode('utf-8')
            file_handler.write(json.dumps({'key': key}))
        print('Master key updated.')
        return True
    else:
        raise ValueError(
            'Fernet key must be 32 url-safe base64-encoded bytes')

def burn():
    """Deletes master key and keys file. Package returns to install state.
    """
    os.remove(master_key_file)
    os.remove(keys_file)
    print('package master key and keys files deleted from disk.')
    print('Please create a new vault instance as this one became useless.')

def view():
    """Prints encrypted values stored in disk."""
    print(json.dumps(vault, indent=4))

def add(app, secrets):
    """
    Encrypts secrets and adds them under a new application.

    :param app: (str) name of the app to add.
    :param secrets: (dict) a Python dictionary containing all key, value
                    pairs to store.

    Example:
    secrets = {'client_id':'123456',
                'client_secret':'iveseenbetter'}
    vault.add('that_app', secrets)
    """
    if type(app) != str or type(secrets) != dict:
        raise TypeError('Unexpected parameter type.')

    if app in vault.keys():
        raise ValueError('This app already exists. Pick a different name.')

    # Encrypt secrets and store added values
    encrypted_secrets = {}
    for key, value in secrets.items():
        cript = Encryption(master_key)
        encrypted_secrets[key] = cript.encrypt(value)
    vault.update({app: encrypted_secrets})
    _update_persistent_vault()

def remove(app):
    """Removes and app entry from the vault. Returns True if value was 
    removed and False otherwise (pehaps item or app don't exist.)
    
    :param app: (str) name of the app entry to remove.
                You can view existing entries by using vault.view()
    """
    if type(app) != str: raise TypeError('Unexpected app value.')
    if app in vault.keys():
        vault.pop(app, None)
        _update_persistent_vault()
        print('App removed from the vault.')
        return True
    else:
        print('No app by that name found in the vault. No action taken.')
        return False

def get(app, item):
    """
    Return the decrypted value of an item in the vault.

    :param app: (str) name of the app in the vault.
    :param item: (str) item identifier in the vault.
    """
    if type(app) != str or type(item) != str:
        raise TypeError('Invalid types.')

    if app not in vault.keys():
        print('App not found. No value returned.')
        return None

    items = vault[app]
    if item not in items.keys():
        print('Item not registered for this app. No value returned.')
        return None

    cripto = Encryption(master_key)
    return cripto.decrypt(vault[app][item])