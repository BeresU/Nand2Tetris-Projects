// passed 

// push: constant: 3030
@3030
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop pointer: THIS

// SP--
@SP
AM=M-1
D=M
@THIS
M=D

// push: constant: 3040
@3040
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop pointer: THAT

// SP--
@SP
AM=M-1
D=M
@THAT
M=D

// push: constant: 32
@32
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THIS 2
@THIS
D=M
@2
D=D+A
@R13
M=D

// SP--
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push: constant: 46
@46
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THAT 6
@THAT
D=M
@6
D=D+A
@R13
M=D

// SP--
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push pointer: THIS
@THIS
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push pointer: THAT
@THAT
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do add

// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M

// push: THIS 2
@THIS
D=M
@2
A=D+A
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do sub

// SP--
@SP
AM=M-1
D=M
A=A-1
M=M-D

// push: THAT 6
@THAT
D=M
@6
A=D+A
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do add

// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
(END)
@END
0;JMP