// FUNCTION: SimpleFunction.test, vars: 2

(SimpleFunction.test)
// RAM[SP] = 0, SP++
@SP
AM=M+1
A=A-1
M=0
// RAM[SP] = 0, SP++
@SP
AM=M+1
A=A-1
M=0
// push: LCL 0
@LCL
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push: LCL 1
@LCL
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
// do not
@SP
A=M-1
M=!M
// push: ARG 0
@ARG
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
// RETURN: current function: SimpleFunction.test
// Put endframe (LCL) in temp variable
@LCL
D=M
@R14
M=D
// Set return address (endframe-5)
@5
A=D-A
D=M
@R13
M=D
// put return value in ARG
// SP--
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// reposition SP, SP=ARG+1 to return value
@ARG
D=M
@SP
M=D+1
// restore THAT = (endframe-1)
@R14
A=M-1
D=M
@THAT
M=D
// restore THIS = (endframe-2)
@R14
D=M
@2
A=D-A
D=M
@THIS
M=D
// restore ARG = (endframe-3)
@R14
D=M
@3
A=D-A
D=M
@ARG
M=D
// restore LCL = (endframe-4)
@R14
D=M
@4
A=D-A
D=M
@LCL
M=D
// return to caller
@R13
A=M
A;JMP