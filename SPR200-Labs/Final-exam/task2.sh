#!/bin/bash

# Specify the file you want to open
SIGNATURE_FILE="client-signature.sig"

# Check if the file exists
if [ -f "$SIGNATURE_FILE" ]; then
    # Display the contents of the file in hexadecimal format
    xxd "$SIGNATURE_FILE"
else
    echo "File does not exist!"
fi
