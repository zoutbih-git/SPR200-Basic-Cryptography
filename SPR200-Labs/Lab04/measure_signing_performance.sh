#!/bin/bash

# Generate a 100MB file
echo "Generating 100MB file..."
dd if=/dev/urandom of=100MB.file bs=1M count=100

# List of hash functions to test
hash_functions=("sha3-256" "sha3-512" "ripemd160")

# Output file for results
output_file="signing_performance.dat"
echo "HashFunction TimeTaken" > $output_file

# Sign the file 100 times for each hash function and measure the average time
for hash in "${hash_functions[@]}"; do
    echo "Testing hash function: $hash"
    total_time=0

    for i in {1..100}; do
        # Measure the time taken to sign the file
        start_time=$(date +%s.%N)
        openssl dgst -$hash -sign private-secp256k1.pem -out 100MB.sig 100MB.file
        end_time=$(date +%s.%N)

        # Calculate the time taken for this iteration
        time_taken=$(echo "$end_time - $start_time" | bc)
        total_time=$(echo "$total_time + $time_taken" | bc)
    done

    # Calculate the average time taken
    average_time=$(echo "scale=3; $total_time / 100" | bc)
    echo "$hash $average_time" >> $output_file
done

echo "Performance measurements saved to $output_file"
