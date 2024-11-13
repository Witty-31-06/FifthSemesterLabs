#!/bin/bash

# Check if a filename is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 filename"
  exit 1
fi

FILE=$1

# Check if the file exists
if [ ! -f "$FILE" ]; then
  echo "File does not exist. Creating file and adding default content."
  # Create file and write default content
  echo "This is a test file with some numbers 123 and words." > "$FILE"
else
  echo "File exists. Proceeding with word and line count."
fi

# Count the number of lines
LINE_COUNT=$(wc -l < "$FILE")

# Count the number of words (including numbers, strings, etc.)
WORD_COUNT=$(wc -w < "$FILE")

# Output the results
echo "Number of lines: $LINE_COUNT"
echo "Number of words: $WORD_COUNT"
