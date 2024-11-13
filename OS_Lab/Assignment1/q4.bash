#!/bin/bash

# Function to check the day of the week for a given date
get_day_of_week() {
    date -d "$1" "+%A"
}

# Function to calculate the difference in years, months, and days between a birthday and today
calculate_age() {
    birth_date=$1

    # Extract the current year and month
    current_year=$(date +%Y)
    current_month=$(date +%m)

    # Extract the birth year and month
    birth_year=${birth_date:0:4}
    birth_month=${birth_date:5:2}

    # Calculate the age in years and months
    age_years=$((current_year - birth_year))
    age_months=$((current_month - birth_month))

    # Adjust if the current month is less than the birth month
    if [ "$age_months" -lt 0 ]; then
        age_years=$((age_years - 1))
        age_months=$((age_months + 12))
    fi

    # Output the age in years and months
    echo "$age_years years, $age_months months"
}



# Read two birthdays from the user
read -p "Enter the first birthday (DD/MM/YYYY): " birthday1
read -p "Enter the second birthday (DD/MM/YYYY): " birthday2

# Convert the input dates to YYYY-MM-DD format for further operations
birthday1_formatted=$(echo "$birthday1" | awk -F/ '{ print $3"-"$2"-"$1 }')
birthday2_formatted=$(echo "$birthday2" | awk -F/ '{ print $3"-"$2"-"$1 }')

# Get the day of the week for both birthdays
day_of_week1=$(get_day_of_week "$birthday1_formatted")
day_of_week2=$(get_day_of_week "$birthday2_formatted")

# Check if the two birthdays match in terms of day of the week
if [ "$day_of_week1" == "$day_of_week2" ]; then
    echo "The two people were born on the same day of the week: $day_of_week1"
else
    echo "The two people were not born on the same day of the week."
    echo "Person 1 was born on a $day_of_week1."
    echo "Person 2 was born on a $day_of_week2."
fi

# Calculate and display the ages of the two people
echo "Person 1's age: $(calculate_age "$birthday1_formatted")"
echo "Person 2's age: $(calculate_age "$birthday2_formatted")"
