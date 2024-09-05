#!/bin/bash

# Check if the file exists
read -p "Enter the file name: " filename
if [[ ! -f $filename ]]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi

# Ask the user for a string (word) to search
read -p "Enter the word to search: " word

# Check if the word is present in the file
occurrences=$(grep -o "\b$word\b" "$filename" | wc -l)

if [[ $occurrences -eq 0 ]]; then
    echo "The word '$word' does not exist in the file."
    exit 1
else
    echo "The word '$word' occurred $occurrences times in total."

    # Display the line numbers and the count of occurrences per line
    echo "Occurrences per line:"
    grep -n "$word" "$filename" | while IFS=: read -r line_number line_content
    do
        line_occurrences=$(echo "$line_content" | grep -o "\b$word\b" | wc -l)
        echo "Line $line_number: $line_occurrences occurrence(s)"
    done
fi
