from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import os

os.chdir("/home/zak/repo/SPR200-Labs/Lab05") #changing working directory
#print("Current Working Directory:", os.getcwd()) #used for debugging

# Load the private key from a file  
with open('private_key_RSA_encrypted_zoutbih.pem', 'rb') as f: #opens file in read mode
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=b'zoutbih',
        backend=default_backend()
    )  



# Load the public key from a file
with open('public_key_RSA_zoutbih.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )  

# Encrypt a file
with open('encrypt_it.txt', 'rb') as f: #change file name to appropriate name
    encrypted = public_key.encrypt( #using the public key variable to encrypt 
        f.read(),
        padding.PKCS1v15() #adding padding due to use of RSA algorithm
    )
# Save the encrypted file
with open('file_encrypted.bin', 'wb') as f: #write the encrypted data to this file
    f.write(encrypted)

# Decrypt the file
with open('file_encrypted.bin', 'rb') as f: #read and decrypt data from the file and save it to the decrypted variable
    decrypted = private_key.decrypt(
        f.read(),
        padding.PKCS1v15()
    )
# Save the decrypted file
with open('file_decrypted.txt', 'wb') as f: #write the decrypted data to this file which is stored in the decrypted variable
    f.write(decrypted)
