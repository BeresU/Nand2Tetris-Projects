// passed

// push: constant: 17
@17
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 17
@17
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do eq

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_EQUAL_0
D;JEQ
@SP
A=M-1
M=0
@CONTINUE_0
0;JMP
(SET_EQUAL_0)
@SP
A=M-1
M=-1
(CONTINUE_0)

// push: constant: 17
@17
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 16
@16
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do eq

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_EQUAL_1
D;JEQ
@SP
A=M-1
M=0
@CONTINUE_1
0;JMP
(SET_EQUAL_1)
@SP
A=M-1
M=-1
(CONTINUE_1)

// push: constant: 16
@16
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 17
@17
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do eq

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_EQUAL_2
D;JEQ
@SP
A=M-1
M=0
@CONTINUE_2
0;JMP
(SET_EQUAL_2)
@SP
A=M-1
M=-1
(CONTINUE_2)

// push: constant: 892
@892
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 891
@891
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
@SET_LOWER_THEN_3
D;JLT
@SP
A=M-1
M=0
@CONTINUE_3
0;JMP
(SET_LOWER_THEN_3)
@SP
A=M-1
M=-1
(CONTINUE_3)

// push: constant: 891
@891
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 892
@892
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
@SET_LOWER_THEN_4
D;JLT
@SP
A=M-1
M=0
@CONTINUE_4
0;JMP
(SET_LOWER_THEN_4)
@SP
A=M-1
M=-1
(CONTINUE_4)

// push: constant: 891
@891
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 891
@891
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
@SET_LOWER_THEN_5
D;JLT
@SP
A=M-1
M=0
@CONTINUE_5
0;JMP
(SET_LOWER_THEN_5)
@SP
A=M-1
M=-1
(CONTINUE_5)

// push: constant: 32767
@32767
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 32766
@32766
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do gt

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_GREATER_THEN_6
D;JGT
@SP
A=M-1
M=0
@CONTINUE_6
0;JMP
(SET_GREATER_THEN_6)
@SP
A=M-1
M=-1
(CONTINUE_6)

// push: constant: 32766
@32766
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 32767
@32767
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do gt

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_GREATER_THEN_7
D;JGT
@SP
A=M-1
M=0
@CONTINUE_7
0;JMP
(SET_GREATER_THEN_7)
@SP
A=M-1
M=-1
(CONTINUE_7)

// push: constant: 32766
@32766
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 32766
@32766
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do gt

// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
@SET_GREATER_THEN_8
D;JGT
@SP
A=M-1
M=0
@CONTINUE_8
0;JMP
(SET_GREATER_THEN_8)
@SP
A=M-1
M=-1
(CONTINUE_8)

// push: constant: 57
@57
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 31
@31
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// push: constant: 53
@53
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

// push: constant: 112
@112
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

// do neg
@SP
A=M-1
M=-M

// do and

// SP--
@SP
AM=M-1
D=M
A=A-1
M=D&M

// push: constant: 82
@82
D=A

// RAM[SP] = D, SP++
@SP
AM=M+1
A=A-1
M=D

// do or

// SP--
@SP
AM=M-1
D=M
A=A-1
M=D|M

// do not
@SP
A=M-1
M=!M
(END)
@END
0;JMP