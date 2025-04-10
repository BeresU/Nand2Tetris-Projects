// passed

// push: constant: 10
@10
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: LCL 0
@LCL
D=M
@R13
M=D

// SP--
@SP
AM=M-1
D=M
@R13
A=M
M=D

// push: constant: 21
@21
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 22
@22
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: ARG 2
@ARG
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

// pop: ARG 1
@ARG
D=M
@1
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

// push: constant: 36
@36
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THIS 6
@THIS
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

// push: constant: 42
@42
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 45
@45
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THAT 5
@THAT
D=M
@5
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

// pop: THAT 2
@THAT
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

// push: constant: 510
@510
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop temp: 6

// SP--
@SP
AM=M-1
D=M
@11
M=D

// push: LCL 0
@LCL
A=M
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: THAT 5
@THAT
D=M
@5
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

// push: ARG 1
@ARG
D=M
@1
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

// push: THIS 6
@THIS
D=M
@6
A=D+A
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: THIS 6
@THIS
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

// do sub

// SP--
@SP
AM=M-1
D=M
A=A-1
M=M-D

// push temp: 6
@11
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