#!/bin/bash

# Define ECC curves to test
ecc_curves=(secp256k1 prime256v1 secp384r1 brainpoolP512t1)
iterations=100
output_file="ecc_keygen_perf.dat"

# Print header to output file
echo "Curve PrivReal PrivUser PrivSys PubReal PubUser PubSys" > "$output_file"

# Function to calculate average time
time_average() {
    local times=($1)
    local sum=0
    for t in "${times[@]}"; do
        sum=$(echo "$sum + $t" | bc -l)
    done
    echo "scale=3; $sum / $iterations" | bc -l
}

# Loop through each curve and measure performance
for curve in "${ecc_curves[@]}"; do
    echo "Measuring performance for $curve..."

    priv_real=()
    priv_user=()
    priv_sys=()
    pub_real=()
    pub_user=()
    pub_sys=()
    
    for ((i=0; i<$iterations; i++)); do
        # Measure private key generation time
        priv_time=$( (time openssl ecparam -genkey -name "$curve" -noout -out private-$curve.pem) 2>&1 )
        priv_real+=( $(echo "$priv_time" | grep real | awk '{print $2}' | sed 's/m/ /;s/s//') )
        priv_user+=( $(echo "$priv_time" | grep user | awk '{print $2}' | sed 's/m/ /;s/s//') )
        priv_sys+=( $(echo "$priv_time" | grep sys | awk '{print $2}' | sed 's/m/ /;s/s//') )
        
        # Measure public key generation time
        pub_time=$( (time openssl ec -in private-$curve.pem -pubout -out public-$curve.pem) 2>&1 )
        pub_real+=( $(echo "$pub_time" | grep real | awk '{print $2}' | sed 's/m/ /;s/s//') )
        pub_user+=( $(echo "$pub_time" | grep user | awk '{print $2}' | sed 's/m/ /;s/s//') )
        pub_sys+=( $(echo "$pub_time" | grep sys | awk '{print $2}' | sed 's/m/ /;s/s//') )
    done
    
    # Calculate averages
    avg_priv_real=$(time_average "${priv_real[*]}")
    avg_priv_user=$(time_average "${priv_user[*]}")
    avg_priv_sys=$(time_average "${priv_sys[*]}")
    avg_pub_real=$(time_average "${pub_real[*]}")
    avg_pub_user=$(time_average "${pub_user[*]}")
    avg_pub_sys=$(time_average "${pub_sys[*]}")
    
# Save results to file, formatting with leading zero
    printf "%s %.3f %.3f %.3f %.3f %.3f %.3f\n" "$curve" "$avg_priv_real" "$avg_priv_user" "$avg_priv_sys" "$avg_pub_real" "$avg_pub_user" "$avg_pub_sys" | tee -a "$output_file"

    # Cleanup temporary keys
    rm -f private-$curve.pem public-$curve.pem

done

echo "Results saved to $output_file"
