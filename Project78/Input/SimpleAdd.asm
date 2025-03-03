// passed 

// push: constant: 7
@7
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 8
@8
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
(END)
@END
0;JMP