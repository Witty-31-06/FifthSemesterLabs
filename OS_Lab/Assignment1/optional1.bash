#!/bin/bash

# Variables
DELETED_FILES_DIR="deleted-files"
LOGFILE="logfile.txt"
USER_NAME=$(whoami)

# Function to log the command
log_command() {
    local command=$1
    echo "$USER_NAME%$command%$(date)" >> $LOGFILE
}

# 1. Display greetings
display_greetings() {
    current_hour=$(date +"%H")
    if [ $current_hour -lt 12 ]; then
        greeting="Good morning"
    else
        greeting="Good evening"
    fi
    echo "Hello $USER_NAME, $greeting!"
    log_command "Display greetings"
}

# 2. List large files
list_large_files() {
    read -p "Enter size in bytes: " size
    echo "Files larger than or equal to $size bytes:"
    echo "---------------------------------------"
    find . -type f -size +"$((size/1024))k" -exec ls -lh {} \; | awk '{print $9 ": " $5}'
    log_command "List large files (size >= $size)"
}

# 3. Disk usage
disk_usage() {
    echo "Disk usage:"
    df -h
    log_command "Disk usage"
}

# 4. View Log File
view_log_file() {
    echo "Log File Contents:"
    echo "---------------------------------------"
    cat $LOGFILE
    log_command "View Log File"
}

# 5. Read an existing file
read_existing_file() {
    read -p "Enter the file name to read: " file_name
    if [ -f "$file_name" ]; then
        cat $file_name
        log_command "Read file $file_name"
    else
        echo "File does not exist."
    fi
}

# 6. Remove an existing file
remove_file() {
    mkdir -p $DELETED_FILES_DIR
    read -p "Enter the file name to delete: " file_name
    if [ -f "$file_name" ]; then
        base_name=$(basename "$file_name")
        dest_file="$DELETED_FILES_DIR/$base_name"
        
        if [ -f "$dest_file" ]; then
            mv "$dest_file" "$dest_file-0"
            mv "$file_name" "$dest_file-1"
        else
            mv "$file_name" "$dest_file"
        fi
        echo "File moved to deleted-files directory."
        log_command "Remove file $file_name"
    else
        echo "File does not exist."
    fi
}

# 6b. Clear deleted-files directory
clear_deleted_files() {
    read -p "Are you sure you want to clear the deleted-files directory? (y/n): " confirm
    if [ "$confirm" == "y" ]; then
        rm -r $DELETED_FILES_DIR/*
        echo "Deleted-files directory cleared."
        log_command "Clear deleted-files directory"
    else
        echo "Operation cancelled."
    fi
}

# Main menu
while true; do
    echo "
    [1] Display greetings
    [2] List large files
    [3] Disk usage
    [4] View Log File
    [5] Read an existing file
    [6] Remove an existing file
        (use -c to clear deleted files directory)
    [7] Exit
    "
    read -p "Your choice > " choice

    case $choice in
        1) display_greetings ;;
        2) list_large_files ;;
        3) disk_usage ;;
        4) view_log_file ;;
        5) read_existing_file ;;
        6) 
            read -p "Enter '-c' to clear or press any key to delete a file: " option
            if [ "$option" == "-c" ]; then
                clear_deleted_files
            else
                remove_file
            fi
            ;;
        7) 
            echo "Exiting..."
            exit 0 ;;
        *)
            echo "Error: Invalid choice. Please select a valid option."
            ;;
    esac
done
