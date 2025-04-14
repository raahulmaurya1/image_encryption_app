import pickle

def save_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# ✅ Save public key in PEM format
def save_public_key_pem(public_key, filename):
    from cryptography.hazmat.primitives import serialization
    with open(filename, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# ✅ Load public key from PEM
def load_public_key_pem(filename):
    from cryptography.hazmat.primitives import serialization
    with open(filename, 'rb') as f:
        return serialization.load_pem_public_key(f.read())
