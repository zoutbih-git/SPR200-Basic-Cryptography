from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

import os

os.chdir("/home/zak/repo/SPR200-Labs/Lab05") #changing working directory
#print("Current Working Directory:", os.getcwd()) #used for debugging

private_key = Ed25519PrivateKey.generate() #private key generation

public_key = private_key.public_key() #public key generation

# Save the private key to a file
with open('private_key_Ed25519_zoutbih.pem', 'wb') as f: #opens and creates a file in write binary mode as a variable f
    f.write(private_key.private_bytes( #converts to bytes
        encoding=serialization.Encoding.PEM, #encoding uses PEM, a cryptographic file format
        format=serialization.PrivateFormat.PKCS8, #format for storing private keys
        encryption_algorithm=serialization.BestAvailableEncryption(b'zoutbih') #the key file is encrypted the password zoutbih
    )   
)
    
# Save the public key to a file
with open('public_key_Ed25519_zoutbih.pem', 'wb') as f: #opens and creates a file in write binary mode as a variable f
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo #format for storing public keys
    )
)
    

#signing the file 

with open('encrypt_it.txt', 'rb') as f:
    signature = private_key.sign(f.read()) #signature variable includes the data from the original file signed
    print("File signed successfully") #print message after successfully signing

# Save the signature to a file
with open('signature.bin', 'wb') as f:
    f.write(signature) #writes the variable to the file
  