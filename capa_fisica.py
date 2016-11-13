# -*- coding: utf-8 -*-
import random
#funcions de codificacio:
#+NRZ  - nrz(seq)
#+NRZL - nrzl(seq)
#+NRZI  - nrzi(seq)
#+bipolar-ami - bami(seq)   
#+pseudoternary - pst(seq)
#+manchester - man(seq)
#+differential manchester - dman(seq)
#+B8ZS - b8zs(seq)
#+HDB3 - hdb3(seq)

# Practica feta amb:
# Alex Bevzenko
# Arnau Sistach

#funcio principal, permet generar seq. i aplicar funcions de cogificacio
def codification(param=1,func=None):
    # param - o longitud de sequencia aleatoria o una lista de 0s i 1s
    seq_init=[]
    n=20
    if type(param)==list:
        seq_init=param
    elif type(param)==int:
        n=param
        for i in range(n):
            seq_init.append(int(random.random()*2)) #random 0s i 1s
    else:#param no valid -agafem n=20
        for i in range(n):
            seq_init.append(int(random.random()*2)) 
    
    if func==None:
        print "usage: codification(sequence or llargada, tipo de codificacion)"
        print "codificacions: nrz, nrzl, nrzi, bami, pst, man, dman, b8zs, hdb3"
        return 0
    print 'dades: '
    print seq_init
    try:
        res=func(seq_init)
        print "codificacio"
        print res
        return res
    except:
        print "invalid codification"
        print "codificacions: nrz, nrzl, nrzi, bami, pst, man, dman, b8zs, hdb3"
    


#Nonreturn Zero basic
# codifiquem 0s com -1 i 1s com 1
def nrz(seq):
    result=[]
    for byte in seq:
        result.append(byte*(2)-1) # -1 - per 0 i 1 per 1
    return result


#Nonreturn Zero - level
# codifiquem 0s com 1 i 1s com -1
def nrzl(seq):
    result=[]
    for byte in seq:
        result.append(byte*(-2)+1) # 1 - per 0 i -1 per 1
    return result


#Nonreturn Zero - inverted
# si tenim bit 0  - ho hi ha canvi de senyal, bit 1 produeix un canvi de -1 a 1 o de 1 a -1
def nrzi(seq):
    result=[] 
    antbyte=seq[0]
    result.append(seq[0]*(2)-1)#nivel inicial de senyal es -1 per bit0 i 1 per bit1
    for byte in range(1, len(seq)):
        if(seq[byte]==1):
            result.append(result[byte-1]*(-1))
            antbyte=seq[byte]
        else:
            result.append(result[byte-1])
    return result


#Bipolar-AMI
# 0 si tenim bit0, bit1 es representa com canvis de nivell de positiu a negatiu
def bami(seq):
    result=[] 
    polarity=1
    for byte in seq:
        if(byte==1):
            result.append(polarity)
            polarity*=-1
        else:
            result.append(0)
    return result


#pseudoternary
# 0 si tenim bit1, bit0 es representa com canvis de nivell de positiu a negatiu
def pst(seq):
    result=[] 
    polarity=1
    for byte in seq:
        if(byte==0):
            result.append(polarity)
            polarity*=-1
        else:
            result.append(0)
    return result


#manchester
#bit0 es representa com canvis de nivell de high a low
#bit1 es representa com canvis de nivell de low a high
def man(seq):
    result=[] 
    for byte in seq:
        if(byte==0):
            result.append((1,0))
        else:
            result.append((0,1))
    return result


#differential manchester
#bit0 es representa com canvi de nivell (high a low) o (low to high) com anterior
#bit1 es representa com canvi diferent del anterior
def dman(seq):
    result=[] 
    if(seq[0]==0):
        result.append((0,1))
        ant=(0,1)
    else:
        result.append((1,0))
        ant=(1,0)

    for byte in range(1, len(seq)):
        if(seq[byte]==1):
            ant=ant[::-1]
            result.append(ant)
        else:
            result.append(ant)
    return result



#B8ZS - Bipolar with 8 Zeros Subs
#igual a BAMI amb modificacio per no perder sync. -
#en cadena de 8 zeros - 8 i 4 tenen polaritat igal a anterior bit1, zeros 7 i 5 tenen polaritat inversa
def b8zs(seq):
    result=[] 
    polarity=1
    cntZero=0
    for byte in seq:
        if(byte==1):
            result.append(polarity)
            polarity*=-1
            cntZero=0
        else:
            result.append(0)
            cntZero+=1
            if cntZero==8:
                result[len(result)-1]=(-1)*polarity
                result[len(result)-2]=polarity
                result[len(result)-4]=polarity
                result[len(result)-5]=(-1)*polarity
                cntZero=0
    return result



#HDB3 - High Density Bit 3
#igual a BAMI amb modificacio per no perder sync. -
#en cadena de 4 zeros  - distingim cadenes senars i parells, substituim:
#senar 000V
#parell B00V amb B - inversa de polaritat anterior, V - igual a pol. anterior
def hdb3(seq):
    result=[] 
    polarity=1
    cntZero=0
    senar=True
    for byte in seq:
        if(byte==1):
            result.append(polarity)
            polarity*=-1
            cntZero=0
        else:
            result.append(0)
            cntZero+=1
            if cntZero==4:
                if senar:
                    result[len(result)-1]=(-1)*polarity
                    senar=False
                else:
                    result[len(result)-4]=polarity
                    result[len(result)-1]=polarity
                    polarity*=-1
                    senar=True
                cntZero=0
    return result




#MODULACIO

# ASK
#solo un plototip de funcio
#A*cos(2pi*f*t) si bit=1
#0 si bit=0
def ask(seq):
    result=[]
    if type(seq[0])==tuple:
        for i in seq:
            for el in i:
                if el!=0:
                    result.append("A*cos(2pi*f*t/2)")
                else:
                    result.append(0)
    else:
        for i in seq:
            if i!=0:
                result.append("A*cos(2pi*f*t)")
            else:
                result.append(0)

    return result
# FSK
#solo un plototip de funcio
#A*cos(2pi*f1*t) si bit=1
#A*cos(2pi*f2*t) si bit=0
def fsk(seq):
    result=[]
    if type(seq[0])==tuple:
        for i in seq:
            for el in i:
                if el!=0:
                    result.append("A*cos(2pi*f1*t/2)")
                else:
                    result.append("A*cos(2pi*f2*t/2)")
    else:
        for i in seq:
            if i!=0:
                result.append("A*cos(2pi*f1*t)")
            else:
                result.append("A*cos(2pi*f2*t)")

    return result


# PSK
#solo un plototip de funcio
#A*cos(2pi*f*t+pi) si bit=1
#A*cos(2pi*f*t) si bit=0
def psk(seq):
    result=[]
    if type(seq[0])==tuple:
        for i in seq:
            for el in i:
                if el!=0:
                    result.append("A*cos(2pi*f*t/2+pi)")
                else:
                    result.append("A*cos(2pi*f*t/2)")
    else:
        for i in seq:
            if i!=0:
                result.append("A*cos(2pi*f*t+pi)")
            else:
                result.append("A*cos(2pi*f*t)")

    return result
