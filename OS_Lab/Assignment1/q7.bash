#!/bin/bash

# Check if the file exists
read -p "Enter the file name: " filename
if [[ ! -f $filename ]]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi

# Ask the user for two patterns (words)
read -p "Enter the word to search for (pattern 1): " pattern1
read -p "Enter the replacement word (pattern 2): " pattern2

# Check if the first pattern exists in the file
occurrences=$(grep -o "\b$pattern1\b" "$filename" | wc -l)

if [[ $occurrences -eq 0 ]]; then
    echo "The word '$pattern1' does not exist in the file."
    exit 1
else
    echo "The word '$pattern1' occurred $occurrences times in total."
    
    # Perform the replacement
    sed -i "s/\b$pattern1\b/$pattern2/g" "$filename"
    
    echo "All occurrences of '$pattern1' have been replaced with '$pattern2'."
    
    # Display a confirmation of the changes
fi
