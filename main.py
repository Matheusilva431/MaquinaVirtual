#16BITS
# OP = opcode → [0-2] 3BITS;
# RD = Registradores de destino → [3-7] 5BITS;
# RS = Registro de fonte 1 → [8-11] 4BITS;
# RT/CONST = Registro de fonte 2/constante → [12-15] 4BITS;
#000 0 0000 0000 0000
#RR ->
#   ADRR -> ROP = 0
#           [ROP] [RS] [RT] [RD]
#   MURR -> ROP = 2
#           [ROP] [RS] [RT] [RD]
#   RRAN -> ROP = 4
#           [ROP] [RS] [RT] [RD]
#RC->
#   SURC -> ROP = 1
#           [ROP] [RD] [RS] [CONST]
#   DIRC -> ROP = 3
#           [ROP] [RD] [RS] [CONST]
#   RCOR -> ROP = 5
#           [ROP] [RD] [RS] [CONST]
#
#REGISTROS -> 10 registradores
#   Vetor contendo valores, posição correspondente ao nome
# @R0, @R1, @R2, @R3, @R4, @R5, @R6, @R7, @R8, @R9

mnemonics = ("ADRR", "SURC", "MURR", "DIRC", "RRAN", "RCOR")
registrador = ("@R0", "@R1", "@R2", "@R3", "@R4", "@R5", "@R6", "@R7", "@R8", "@R9")
msg_erro = ("ERRO --> OPCODE Não é conhecido", "ERRO --> Registrador não existe")

registradores = []
rop = rs = rt = rd = const = -1

def fetch(instrucoes, pc):
    return instrucoes[pc]

def decode(instrucao):
    global rop, rs, rt, rd, const
    rop = (instrucao & 0b1110000000000000) >> 13
    if rop > 6:
        return 0
    else:
        rd = (instrucao & 0b0001111100000000) >> 8#pega o regitrador que irá receber o valor
        rs = (instrucao & 0b0000000011110000) >> 4#pega o registrador 1
        rt = const = (instrucao & 0b0000000000001111) >> 0#Pega a contante ou o regitrador 2

        if rd > 9 or rs > 9:
            return 1

        if rop % 2 ==0:
            rc = False
            if rt > 9:
                return 1
        else:
            rc = True

    mostrains(rop, rd, rs, rt, rc)
    return 2

def mostrains(rop, rd, rs, rt, rc = False):
    if rc:
        print("Instrucao --> ", mnemonics[rop], " ", registrador[rd], " ", registrador[rs], " ", rt)
    else:
        print("Instrucao --> ", mnemonics[rop], " ", registrador[rs], " ", registrador[rt], " ", registrador[rd])

def execute():
    print("Opcode: {0:03b} --> {0}".format(rop, rop))
    if rop % 2 == 0:
        print("Registro Antes:")
        print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        print("RS -> {0:04b}: ".format(rs) + str(registrador[rs]) + " = " + str(registradores[rs]))
        print("RT -> {0:04b}: ".format(rt) + str(registrador[rt]) + " = " + str(registradores[rt]))
        print("Registro Depois:")
        if rop == 0:#ADRR
            registradores[rd] = registradores[rs] + registradores[rt]
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        elif rop == 2:#MURR
            registradores[rd] = registradores[rs] * registradores[rt]
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        elif rop == 4:#RRAN
            registradores[rd] = registradores[rs] & registradores[rt]
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
            print("Operacao")
            print("RS: {0:04b}".format(registradores[rs]))
            print("RT: {0:04b}".format(registradores[rt]))
            print("RD: {0:04b}".format(registradores[rd]))

    else:
        print("Registro Antes:")
        print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        print("RS -> {0:04b}: ".format(rs) + str(registrador[rs]) + " = " + str(registradores[rs]))
        print("Constante -> {0:04b}: ".format(rt) + str(const))
        print("Registro Depois:")
        if rop == 1:#SURC
            registradores[rd] = registradores[rs] - const
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        elif rop == 3:#DIRC
            registradores[rd] = registradores[rs] / const
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
        elif rop == 5:#RCOR
            registradores[rd] = registradores[rs] | const
            print("RD -> {0:05b}: ".format(rd) + str(registrador[rd]) + " = " + str(registradores[rd]))
            print("Operacao")
            print("RS: {0:04b}".format(registradores[rs]))
            print("RT: {0:04b}".format(registradores[rt]))
            print("RD: {0:04b}".format(registradores[rd]))

    print()

def initRegistradores():
    for i in range(10):
        registradores.append(i)

#main
instrucoes = [0b0000000001101001, 0b0010000101110001, 0b0100001010000001,
              0b0110001110011010, 0b1000010001110001, 0b1010010110010101]
pc = 0

initRegistradores()
numInstrucao = 6
while pc < 6:
    ir = fetch(instrucoes, pc)
    res = decode(ir)
    if res < 2:
        print(msg_erro[res])
    else:
        execute()
    pc = pc + 1
for i in range(10):
    print("@R[", i, "]: ", registradores[i])


