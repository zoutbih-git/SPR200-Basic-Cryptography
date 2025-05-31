#!/usr/bin/env python3

import argparse
import os #imports the os module
import binascii
import pyspx.shake_128f as sphincs #imports the SPHINCS+ shake_128f cryptographic module, you need to create a virtual environment first, python3 -m venv .venv (.venv is the name), then you need to activate it source .venv/bin/activate, once activated the terminal will change to reflect working in a virtual environment. To exit the virtual environment and use system environment use the deactivate command. Use pip list to see installed packages in the virtual environment.




def keygen():
    """Generate a SPHINCS+ keypair and save to files."""
    try:
        # Generate a random seed 
        seed = os.urandom(sphincs.crypto_sign_SEEDBYTES) #length of the seed is set by the constant crypto_sign_SEEDBYTES from the pyspx.shake_128f module, ensuring that the seed size matches the expected size for the SPHINCS+ cryptographic algorithm. The pyspx.shake_128f.crypto_sign_SEEDBYTES constant is 48
#print(pyspx.shake_128f.crypto_sign_SEEDBYTES) # value is 48


        # Generate a new keypair
        keys = sphincs.generate_keypair(seed) #creates a public and a private key using the random seed value, in order to make cryptographically random and secure seeds.
        public_key = keys[0] #public key
        private_key = keys[1] #private key

        
        # Convert keys to hex for storage
        public_key_hex = binascii.hexlify(public_key).decode('ascii') #converts to ascii for better readability
        private_key_hex = binascii.hexlify(private_key).decode('ascii')
        
        # Save public key key to files
        try:
            with open('public_key.hex', 'w') as f:
                f.write(public_key_hex)
        except IOError as e:
            print(f"Error writing public key file: {e}")
            return
            
        # Save private key to files
        with open('private_key.hex', 'w') as f:
            f.write(private_key_hex)

        # Print the keypair generation information
        print("Keypair generated:")
        print(f"- Public key: public_key.hex")
        print(f"- Private key: private_key.hex")

    except Exception as e:
        print(f"Error generating keypair: {e}")

def sign(file_path):
    """Sign a file using SPHINCS+ and save the signature to a file."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return
        
        # Load the private key
        if not os.path.exists('private_key.hex'):
            print("Error: Private key not found. Run --keygen first.")
            return
        
        try:
            with open('private_key.hex', 'r') as f:
                private_key_hex = f.read().strip()  # why we need to strip here?
        except IOError as e:
            print(f"Error reading private key file: {e}")
            return


        private_key = binascii.unhexlify(private_key_hex)


        # Read the file content
        with open(file_path, 'rb') as f:
            message = f.read()

        # Sign the message
        signature = sphincs.sign(message, private_key) #signs the message variable using the private_key must be message, private_key in that order

        # Convert signature to hex and save to file
        signature_hex = binascii.hexlify(signature).decode('ascii')
        try:
            with open('signature.hex', 'w') as f:
                f.write(signature_hex)
        except IOError as e:
            print(f"Error writing signature file: {e}")
            return

        # Print the signature generation information
        print("Signature generated:")
        print(f"- Signature: signature.hex")
    except Exception as e:
        print(f"Error signing file: {e}")

def verify(file_path, signature_path, public_key_path):
    """Verify a file's signature using SPHINCS+."""
    try:
        # Check if all files exist
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return
        
        if not os.path.exists(public_key_path):
            print(f"Error: Public key file '{public_key_path}' not found.")
            return

        # Load the public key
        try:
            with open(public_key_path, 'r') as f:
                public_key_hex = f.read().strip()
        except IOError as e:
            print(f"Error reading public key file: {e}")
            return
        
        # Load the signature
        try:
            with open(signature_path, 'r') as f:
                signature_hex = f.read().strip()
        except IOError as e:
            print(f"Error reading signature file: {e}")
            return
        
        # Read the file content
        try:
            with open(file_path, 'rb') as f:
                message = f.read()
        except IOError as e:
            print(f"Error reading file to verify: {e}")
            return
        
        # Convert hex to bytes
        try:
            public_key = binascii.unhexlify(public_key_hex)
            signature = binascii.unhexlify(signature_hex)
        except binascii.Error as e:
            print(f"Error decoding hex data: {e}")
            return
        
        # Verify the signature
        try:
            result = sphincs.verify(message, signature, public_key)
            print(f"Signature Verification result: {result}")
        except Exception as e:
            print(f"Signature Verification result: False")
            print(f"Error during verification: {str(e)}")
    except Exception as e:
        print(f"Error verifying signature: {e}")

def main():
    try:
        parser = argparse.ArgumentParser(description='SPHINCS+ Digital Signature Tool')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--keygen', action='store_true', help='Generate a new keypair')
        group.add_argument('--sign', metavar='FILE', help='Sign the specified file')
        group.add_argument('--verify', metavar='FILE', help='Verify a signature for the specified file')
        
        parser.add_argument('signature', nargs='?', help='Path to the signature file (for --verify)')
        parser.add_argument('public_key', nargs='?', help='Path to the public key file (for --verify)')
        
        args = parser.parse_args()
        
        if args.keygen:
            keygen()
        elif args.sign:
            sign(args.sign)
        elif args.verify:
            if not args.signature or not args.public_key:
                parser.error("--verify requires signature and public_key paths")
            verify(args.verify, args.signature, args.public_key)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()  
