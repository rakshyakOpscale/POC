#!/bin/bash

echo "Reading from:"
echo $1

filename=$1 # Get file from command line argument
max_attempts=8
counter=0

# Check if the file exists
if [ -f "$filename" ]; then
    echo "File exists. Reading contents:"
    cat "$filename"
else
    echo "File does not exist. Waiting for it to be created..."

    # Loop until the file is created or maximum attempts reached
    while [ $counter -lt $max_attempts ] && [ ! -f "$filename" ]; do
        sleep 1  # Wait for 1 second before checking again
        counter=$((counter + 1))
    done

    if [ -f "$filename" ]; then
        echo "File created. Reading contents:"
        cat "$filename"
    else
        echo "File not found after $max_attempts attempts."
    fi
fi