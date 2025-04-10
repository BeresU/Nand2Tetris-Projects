// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.


(MAIN_LOOP)

    // Check if space pressed

    @R0
    M=0

    @KBD
    D=M

    @32     // SPACE
    D=D-A

    // If space pressed set R0 to -1
    @FILL_SCREEN    
    D;JNE   

    @R0
    M=-1

    (FILL_SCREEN)

        // Initialize the screen loop
        @i
        M=0
        @SCREEN
        D=A
        @addr   // Set addr to the screen base address
        M=D
        @8192   // Screen chunk size 
        D=A
        @n      
        M=D

        (FILL_SCREEN_LOOP)
            @i
            D=M
            @n
            D=M-D   
            @MAIN_LOOP
            D;JEQ
            
            // Set the pixel according to the press value
            @R0
            D=M
            @addr
            A=M
            M=D

            @i
            M=M+1   // i++
            @addr
            M=M+1  // addr = addr + 1

            @FILL_SCREEN_LOOP
            0;JMP

    @MAIN_LOOP
    0;JMP


