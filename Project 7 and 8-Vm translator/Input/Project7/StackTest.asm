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
// EQ
// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
D=D+1
@1
D=D&A
@SP
A=M-1
M=-D
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
// EQ
// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
D=D+1
@1
D=D&A
@SP
A=M-1
M=-D
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
// EQ
// SP--
@SP
AM=M-1
D=M
A=A-1
D=M-D
D=D+1
@1
D=D&A
@SP
A=M-1
M=-D
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
M=0
@END_LOWER_THEN_1
D;JGE
@SP
A=M-1
M=-1

(END_LOWER_THEN_1)
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
M=0
@END_LOWER_THEN_2
D;JGE
@SP
A=M-1
M=-1

(END_LOWER_THEN_2)
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
M=0
@END_LOWER_THEN_3
D;JGE
@SP
A=M-1
M=-1

(END_LOWER_THEN_3)
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
M=0
@END_GREATER_THEN_1
D;JLE
@SP
A=M-1
M=-1

(END_GREATER_THEN_1)
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
M=0
@END_GREATER_THEN_2
D;JLE
@SP
A=M-1
M=-1

(END_GREATER_THEN_2)
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
M=0
@END_GREATER_THEN_3
D;JLE
@SP
A=M-1
M=-1

(END_GREATER_THEN_3)
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