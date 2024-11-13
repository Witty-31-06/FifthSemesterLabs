#!/bin/bash

# Count ordinary files (excluding directories) in the current directory and subdirectories
FILE_COUNT=$(find . -type f | wc -l)

# Count directories (excluding ordinary files) in the current directory and subdirectories
DIR_COUNT=$(find . -type d | wc -l)

# Output the results
echo "Number of ordinary files: $FILE_COUNT"
echo "Number of directories: $DIR_COUNT"
