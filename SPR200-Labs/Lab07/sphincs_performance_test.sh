#!/bin/bash

# Performance comparison between SPHINCS+ and ECC (secp128r1)
# Requires `openssl` (for ECC) and `pyspx` (for SPHINCS+)

# Check dependencies
if ! command -v openssl &> /dev/null; then
    #uses command -v to check if the openssl command is in the system path, uses negation	
    echo "Error: OpenSSL not installed. Install it first."
    exit 1
fi

if ! python3 -c "import pyspx.shake_128f" &> /dev/null; then #checks if pyspx is installed by importing
    echo "Error: pyspx not installed in Python environment."
    exit 1
fi

# Function to measure execution time
measure_time() { #bash function used to measure the time a command takes
    local start_time=$(date +%s.%N) # local variable gives date, seconds and nanoseconds
    "$@" 
    local end_time=$(date +%s.%N)
    echo "$(echo "$end_time - $start_time" | bc)" #calculates the difference between end_time and start_time, sends it to basic calculator
}

# Generate a random message
MESSAGE_FILE="message.txt" #file for testing signatures
echo "Performance test message for SPHINCS+ and ECC (secp128r1)" > "$MESSAGE_FILE" #echo message into file

#SPHINCS+ TEST
echo "Running SPHINCS+ tests..."

SPHINCS_PUB="sphincs_public_key.hex" #public key file 
SPHINCS_PRIV="sphincs_private_key.hex" #private key file
SPHINCS_SIG="sphincs_signature.hex" #signature file

#these commands measure the time it takes to create a public key and secret key
SPHINCS_KEYGEN_TIME=$(measure_time python3 -c "
import os, binascii, pyspx.shake_128f as sphincs
seed = os.urandom(sphincs.crypto_sign_SEEDBYTES)
pk, sk = sphincs.generate_keypair(seed)
open('$SPHINCS_PUB', 'w').write(binascii.hexlify(pk).decode())
open('$SPHINCS_PRIV', 'w').write(binascii.hexlify(sk).decode())
")


#these commands measure the time it takes to use the .sign function in order to sign the message file
SPHINCS_SIGN_TIME=$(measure_time python3 -c "
import binascii, pyspx.shake_128f as sphincs 
sk = binascii.unhexlify(open('$SPHINCS_PRIV').read().strip()) 
msg = open('$MESSAGE_FILE', 'rb').read()
sig = sphincs.sign(msg, sk)
open('$SPHINCS_SIG', 'w').write(binascii.hexlify(sig).decode())
")

#these commands measure the time it takes to use the verify function with the parameters msg, sig, pk to verify the signature
SPHINCS_VERIFY_TIME=$(measure_time python3 -c "
import binascii, pyspx.shake_128f as sphincs
pk = binascii.unhexlify(open('$SPHINCS_PUB').read().strip())
sig = binascii.unhexlify(open('$SPHINCS_SIG').read().strip())
msg = open('$MESSAGE_FILE', 'rb').read()
result = sphincs.verify(msg, sig, pk)
")

#ECC (secp128r1) TEST
echo "Running ECC tests..."

ECC_PRIV="ecc_private.pem" #private key file
ECC_PUB="ecc_public.pem" #public key file
ECC_SIG="ecc_signature.bin" #signature file

#creation of the private key and measurement
ECC_KEYGEN_TIME=$(measure_time openssl ecparam -name secp128r1 -genkey -noout -out "$ECC_PRIV")

#public key extraction and time measurement
ECC_PUB_TIME=$(measure_time openssl ec -in "$ECC_PRIV" -pubout -out "$ECC_PUB")

#signing of the message file and time measurement
ECC_SIGN_TIME=$(measure_time openssl dgst -shake128 -sign "$ECC_PRIV" -out "$ECC_SIG" "$MESSAGE_FILE")

#verifying the file signature and measurement
ECC_VERIFY_TIME=$(measure_time openssl dgst -shake128 -verify "$ECC_PUB" -signature "$ECC_SIG" "$MESSAGE_FILE" -noout)


# Extract only the numerical time value from ECC_VERIFY_TIME
ECC_VERIFY_TIME_NUM=$(echo "$ECC_VERIFY_TIME" | awk '{print $NF}')
echo $ECC_VERIFY_TIME_NUM

#OUTPUT RESULTS
echo "Performance results:"
echo "SPHINCS+      - KeyGen: $SPHINCS_KEYGEN_TIME s, Sign: $SPHINCS_SIGN_TIME s, Verify: $SPHINCS_VERIFY_TIME s"
echo "secp128r1 - KeyGen: $ECC_KEYGEN_TIME s, Sign: $ECC_SIGN_TIME s, Verify: $ECC_VERIFY_TIME_NUM s"

# Write to signing_performance.dat
echo "Algorithm KeyGen Sign Verify" > signing_performance.dat
echo "SPHINCS+ $SPHINCS_KEYGEN_TIME $SPHINCS_SIGN_TIME $SPHINCS_VERIFY_TIME" >> signing_performance.dat
echo "secp128r1 $ECC_KEYGEN_TIME $ECC_SIGN_TIME $ECC_VERIFY_TIME_NUM" >> signing_performance.dat

echo "Results saved to performance_results.csv and signing_performance.dat"
