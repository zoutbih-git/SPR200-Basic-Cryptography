from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

import os

os.chdir("/home/zak/repo/SPR200-Labs/Lab05") #changing working directory
#print("Current Working Directory:", os.getcwd()) #used for debugging


# Load the public key from a file
with open('public_key_Ed25519_zoutbih.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key( #returns an object public_key with the below parameters
        f.read(),
        backend=default_backend()
    )

# load the signature file
with open('signature.bin', 'rb') as f:
    signature = f.read() #reads the signature from the file and saves it as the variable signaure

try:   
    with open('encrypt_it.txt', 'rb') as f:
        public_key.verify(signature, f.read()) #verify method using signature variable and data from file to ensure the file was unchanged
        print("signature verification successfull")
                 
except InvalidSignature: #if data is changed in the file it will throw an exception
    print("signature verification failed")

