@256
D=A
@SP
M=D
// call function: Sys.init, args: 0
// save return address
@Sys.init$ret.1
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push LCL of current segment
@LCL
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push ARG of current segment
@ARG
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THIS of current segment
@THIS
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THAT of current segment
@THAT
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// ARG=SP-5-0
@SP
D=M
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP

(Sys.init$ret.1)
// FUNCTION: Main.fibonacci, vars: 0

(Main.fibonacci)
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
// do lt
// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@Main.Main.fibonacci$SET_LOWER_THEN_1
D;JLT
@SP
A=M-1
M=0
@Main.Main.fibonacci$CONTINUE_1
0;JMP

(Main.Main.fibonacci$SET_LOWER_THEN_1)
@SP
A=M-1
M=-1

(Main.Main.fibonacci$CONTINUE_1)
// if-goto Main.Main.fibonacci$N_LT_2
// SP--
@SP
AM=M-1
D=M
@Main.Main.fibonacci$N_LT_2
D;JNE
// goto N_GE_2
@Main.Main.fibonacci$N_GE_2
0;JMP

(Main.Main.fibonacci$N_LT_2)
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// RETURN: current function: Main.fibonacci
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

(Main.Main.fibonacci$N_GE_2)
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
// call function: Main.fibonacci, args: 1
// save return address
@Main.fibonacci$ret.1
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push LCL of current segment
@LCL
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push ARG of current segment
@ARG
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THIS of current segment
@THIS
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THAT of current segment
@THAT
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// ARG=SP-5-1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP

(Main.fibonacci$ret.1)
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
// call function: Main.fibonacci, args: 1
// save return address
@Main.fibonacci$ret.2
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push LCL of current segment
@LCL
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push ARG of current segment
@ARG
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THIS of current segment
@THIS
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THAT of current segment
@THAT
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// ARG=SP-5-1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP

(Main.fibonacci$ret.2)
// do add
// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
// RETURN: current function: Main.fibonacci
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
// FUNCTION: Sys.init, vars: 0

(Sys.init)
// push: constant: 4
@4
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// call function: Main.fibonacci, args: 1
// save return address
@Main.fibonacci$ret.3
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push LCL of current segment
@LCL
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push ARG of current segment
@ARG
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THIS of current segment
@THIS
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push THAT of current segment
@THAT
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// ARG=SP-5-1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP

(Main.fibonacci$ret.3)

(Sys.Sys.init$END)
// goto END
@Sys.Sys.init$END
0;JMP