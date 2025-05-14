// FUNCTION: Sys.init, vars: 0

(Sys.init)
// push: constant: 4000
@4000
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
// push: constant: 5000
@5000
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
// call function: Sys.main, args: 0
// save return address
@Sys.main$ret.1
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
@Sys.main
0;JMP

(Sys.main$ret.1)
// pop temp: 1
// SP--
@SP
AM=M-1
D=M
@6
M=D

(Sys.Sys.init$LOOP)
// goto LOOP
@Sys.Sys.init$LOOP
0;JMP
// FUNCTION: Sys.main, vars: 5

(Sys.main)
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
// RAM[SP] = 0, SP++
@SP
AM=M+1
A=A-1
M=0
// push: constant: 4001
@4001
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
// push: constant: 5001
@5001
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
// push: constant: 200
@200
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// pop: LCL 1
@LCL
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
// push: constant: 40
@40
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// pop: LCL 2
@LCL
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
// push: constant: 6
@6
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// pop: LCL 3
@LCL
D=M
@3
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
// push: constant: 123
@123
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// call function: Sys.add12, args: 1
// save return address
@Sys.add12$ret.1
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
@Sys.add12
0;JMP

(Sys.add12$ret.1)
// pop temp: 0
// SP--
@SP
AM=M-1
D=M
@5
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
// push: LCL 2
@LCL
D=M
@2
A=D+A
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push: LCL 3
@LCL
D=M
@3
A=D+A
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push: LCL 4
@LCL
D=M
@4
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
// do add
// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
// do add
// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
// do add
// SP--
@SP
AM=M-1
D=M
A=A-1
M=D+M
// RETURN: current function: Sys.main
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
// FUNCTION: Sys.add12, vars: 0

(Sys.add12)
// push: constant: 4002
@4002
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
// push: constant: 5002
@5002
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
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push: constant: 12
@12
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
// RETURN: current function: Sys.add12
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