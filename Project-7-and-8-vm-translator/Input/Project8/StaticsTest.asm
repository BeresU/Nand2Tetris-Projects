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
// FUNCTION: Class1.set, vars: 0

(Class1.set)
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// pop static: Class1.0
// SP--
@SP
AM=M-1
D=M
@Class1.0
M=D
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
// pop static: Class1.1
// SP--
@SP
AM=M-1
D=M
@Class1.1
M=D
// push: constant: 0
@0
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// RETURN: current function: Class1.set
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
// FUNCTION: Class1.get, vars: 0

(Class1.get)
// push static: Class1.0
@Class1.0
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push static: Class1.1
@Class1.1
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
// RETURN: current function: Class1.get
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
// FUNCTION: Class2.set, vars: 0

(Class2.set)
// push: ARG 0
@ARG
A=M
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// pop static: Class2.0
// SP--
@SP
AM=M-1
D=M
@Class2.0
M=D
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
// pop static: Class2.1
// SP--
@SP
AM=M-1
D=M
@Class2.1
M=D
// push: constant: 0
@0
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// RETURN: current function: Class2.set
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
// FUNCTION: Class2.get, vars: 0

(Class2.get)
// push static: Class2.0
@Class2.0
D=M
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push static: Class2.1
@Class2.1
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
// RETURN: current function: Class2.get
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
// push: constant: 6
@6
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
// call function: Class1.set, args: 2
// save return address
@Class1.set$ret.1
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
// ARG=SP-5-2
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP

(Class1.set$ret.1)
// pop temp: 0
// SP--
@SP
AM=M-1
D=M
@5
M=D
// push: constant: 23
@23
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// push: constant: 15
@15
D=A
// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D
// call function: Class2.set, args: 2
// save return address
@Class2.set$ret.1
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
// ARG=SP-5-2
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP

(Class2.set$ret.1)
// pop temp: 0
// SP--
@SP
AM=M-1
D=M
@5
M=D
// call function: Class1.get, args: 0
// save return address
@Class1.get$ret.1
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
@Class1.get
0;JMP

(Class1.get$ret.1)
// call function: Class2.get, args: 0
// save return address
@Class2.get$ret.1
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
@Class2.get
0;JMP

(Class2.get$ret.1)

(Sys.Sys.init$END)
// goto END
@Sys.Sys.init$END
0;JMP