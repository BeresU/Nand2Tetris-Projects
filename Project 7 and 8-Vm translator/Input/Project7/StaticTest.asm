//passed 

// push: constant: 111
@111
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 333
@333
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 888
@888
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop static: StaticTest.8

// SP--
@SP
AM=M-1
D=M
@StaticTest.8
M=D

// pop static: StaticTest.3

// SP--
@SP
AM=M-1
D=M
@StaticTest.3
M=D

// pop static: StaticTest.1

// SP--
@SP
AM=M-1
D=M
@StaticTest.1
M=D

// push static: StaticTest.3
@StaticTest.3
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push static: StaticTest.1
@StaticTest.1
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

// push static: StaticTest.8
@StaticTest.8
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