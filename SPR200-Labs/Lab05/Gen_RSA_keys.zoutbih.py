#Lab 5 Using Python and Python Libraries for cryptographic tasks
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

os.chdir("/home/zak/repo/SPR200-Labs/Lab05") #changing working directory

# Generate a new RSA keys with 2048 bits, and use public exponent 65537
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Get the public key 
public_key = private_key.public_key()



# Save the private key to a file
with open('private_key_RSA_encrypted_zoutbih.pem', 'wb') as f: #opens and creates a file in write binary mode as a variable f
    f.write(private_key.private_bytes( #converts to bytes
        encoding=serialization.Encoding.PEM, #encoding uses PEM, a cryptographic file format
        format=serialization.PrivateFormat.PKCS8, #format for storing private keys
        encryption_algorithm=serialization.BestAvailableEncryption(b'zoutbih') #the key file is encrypted the password zoutbih
    )   
)

# Save the public key to a file
with open('public_key_RSA_zoutbih.pem', 'wb') as f: #opens and creates a file in write binary mode as a variable f
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo #format for storing public keys
    )
)
    
#print("Current Working Directory:", os.getcwd()) #used for debugging