from .vault import Vault as vault # to keep previous version working.

"""
The below method copies of vault were implemented in case one doesn't want to
create a vault.
"""
internal_vault = vault()
def replace_master_key(key):
    return internal_vault.replace_master_key(key)

def burn():
    internal_vault.burn()

def view():
    internal_vault.view()

def add(app, secrets):
    internal_vault.add(app, secrets)

def remove(app):
    return internal_vault.remove(app)

def get(app, item):
    return internal_vault.get(app, item)