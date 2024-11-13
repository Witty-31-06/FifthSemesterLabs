.model small
.stack 100h

.data
    msg1 db 10, 13, "Enter a character: $"
    msg2 db 10, 13, "The character you entered is: $"

.code
main proc
    ; Initialize the data segment
         mov ax, @data
         mov ds, ax

    ; Display the input prompt
         lea dx, msg1
         mov ah, 09h
         int 21h

    ; Accept a character from the keyboard
         mov ah, 01h
         int 21h
    ; The character entered is now in the AL register

    ; Display the output prompt
         lea dx, msg2
         mov ah, 09h
         int 21h

    ; Display the character entered
         mov dl, al       ; Move the character from AL to DL for printing
         mov ah, 02h
         int 21h

    ; Terminate the program
         mov ah, 4ch
         int 21h

main endp
end main