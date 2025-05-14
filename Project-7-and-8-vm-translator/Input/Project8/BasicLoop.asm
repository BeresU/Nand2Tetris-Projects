// push: constant: 0
@0
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

(BasicLoop$LOOP)
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
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
// do add
// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
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
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// if-goto BasicLoop$LOOP
// SP--
@SP
AM=M-1
D=M
@BasicLoop$LOOP
D;JNE
// push: LCL 0
@LCL
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D