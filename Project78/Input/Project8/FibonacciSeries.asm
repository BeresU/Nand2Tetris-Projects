// passed 
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

// pop pointer: THAT

// SP--
@SP
AM=M-1
D=M
@THAT
M=D

// push: constant: 0
@0
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THAT 0
@THAT
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

// push: constant: 1
@1
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// pop: THAT 1
@THAT
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

// push: ARG 0
@ARG
A=M
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 2
@2
D=A

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

// pop: ARG 0
@ARG
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
(FibonacciSeries$LOOP)

// push: ARG 0
@ARG
A=M
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// if-goto FibonacciSeries$COMPUTE_ELEMENT

// SP--
@SP
AM=M-1
D=M
@FibonacciSeries$COMPUTE_ELEMENT
D;JNE

// goto END
@FibonacciSeries$END
0;JMP
(FibonacciSeries$COMPUTE_ELEMENT)

// push: THAT 0
@THAT
A=M
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: THAT 1
@THAT
D=M
@1
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

// push pointer: THAT
@THAT
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 1
@1
D=A

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

// pop pointer: THAT

// SP--
@SP
AM=M-1
D=M
@THAT
M=D

// push: ARG 0
@ARG
A=M
D=M

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 1
@1
D=A

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

// pop: ARG 0
@ARG
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

// goto LOOP
@FibonacciSeries$LOOP
0;JMP
(FibonacciSeries$END)