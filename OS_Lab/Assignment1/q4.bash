#!/bin/bash

# Function to check the day of the week for a given date
get_day_of_week() {
    date -d "$1" "+%A"
}

# Function to calculate the difference in years, months, and days between a birthday and today
calculate_age() {
    birth_date=$1
    today=$(date +%Y-%m-%d)
    age=$(echo "$today" | awk -F- -v bdate="$birth_date" '
    {
        byear=substr(bdate, 1, 4)
        bmonth=substr(bdate, 6, 2)
        bday=substr(bdate, 9, 2)

        tyear=$1
        tmonth=$2
        tday=$3

        # Calculate year difference
        years=tyear - byear
        months=tmonth - bmonth
        days=tday - bday

        # Adjust for month and day differences
        if (months < 0) {
            years--
            months += 12
        }
        if (days < 0) {
            months--
            days += 30  # Rough estimation for days in month
        }

        print years " years, " months " months, " days " days"
    }')
    echo "$age"
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
