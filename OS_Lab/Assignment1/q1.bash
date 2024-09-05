#!/bin/bash

# Read user input for uv1 and uv2
read -p "Enter the value for uv1: " uv1
read -p "Enter the value for uv2: " uv2

# Function to reverse a string
reverse() {
  echo "$1" | rev
}

# Reverse and print uv1 and uv2
echo "Reversed uv1: $(reverse $uv1)"
echo "Reversed uv2: $(reverse $uv2)"


is_number() {
  if [[ $1 =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
    return 0
  else
    return 1  
  fi
}


if is_number "$uv1" && is_number "$uv2"; then
  sum=$(echo "$uv1 + $uv2" | bc)
  echo "The sum of uv1 and uv2 is: $sum"
else
  echo "Error: One or both variables are not valid numbers, so they cannot be added."
fi
