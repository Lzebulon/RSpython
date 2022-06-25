from gf import GF
from gf256 import *
from gf256int import *
from polynome import *
from polynomeGF import *

class ReedSolomon:
    def __init__(self,n,k):
        self.field = GF256(2,8)
        self.n = n
        self.k = k
        self.t = n-k
        self.g = self.genPoly(n-k)

    def genPoly(self,errSize):
        polynome = Polynomial([GF256int(1)])

        for i in range(1,errSize+1):
            polynome = polynome * Polynomial([GF256int(self.field._GFEXP[i]),GF256int(1)])
        
        return polynome

    def encode(self, message):
        if isinstance(message[0],int): message = [GF256int(x) for x in message][::-1]
        elif isinstance(message[0],str) : message = [GF256int(ord(x)) for x in message][::-1]
        elif not isinstance(message[0],GF256int) : raise NotImplemented
        if not isinstance(message,Polynomial): message = Polynomial(message)
        t = Polynomial([GF256int(0)]*(self.n-self.k)+message.coefficients)
        return t + (t % self.g)


    def syndrome(self,msg,errSize):
        syndrome = Polynomial([GF256int(0)]*(errSize+1))

        for i in range(1,errSize+1):
            syndrome[i] = msg.evaluate(GF256int(self.field._GFEXP[i]))
        return syndrome


    def errorLocator(self,syndrome):
        C = Polynomial([GF256int(1)])
        B = Polynomial([GF256int(1)])
        L = 0
        x = 1
        b = GF256int(1)

        for n in range(syndrome.len()):
            d = GF256int(0)

            for i in range(1,L+1):
                d += C[i]* syndrome[n-i]
            d += syndrome[n]

            if d == GF256int(0):
                x += 1
            elif 2*L <= n:
                T = Polynomial(list(C.coefficients))
                C = C - B * Polynomial([GF256int(0) for _ in range(x)] + [GF256int(1)]) * d * b.inverse()
                L = n+1 - L
                B = T
                b = d
                x = 1
            else :
                C = C - B * Polynomial([GF256int(0) for _ in range(x)] + [GF256int(1)]) * d * b.inverse()
                x += 1
        return C[:L:]

    def errorPosition(self,errLoc):
        errPos = []
        for i in range(256):
            if errLoc.evaluate(GF256int(i)) == GF256int(0):
                errPos.append(self.field._GFLOG[GF256int(i).inverse().value])
        return errPos


    def errorEvaluator(self, syndrome, errLoc):
        mul = syndrome[1::] * errLoc

        return mul[:self.t:]


    def errorPolynomial(self,syndrome,errLoc,errPos):
        errEval = self.errorEvaluator(syndrome,errLoc)
        errLocDerivate = Polynomial([ errLoc[i+1] if i%2 == 0 else GF256int(0) for i in range(errLoc.len()-1)])
        errorPolynomial = Polynomial([GF256int(0)]*(max(errPos) + 1))

        for pos in errPos : 
            xInv = GF256int(self.field._GFEXP[pos]).inverse()
            magnitude = errEval.evaluate(xInv) / errLocDerivate.evaluate(xInv)
            errorPolynomial[pos] = magnitude
        
        return errorPolynomial


    def decode(self, message, errSize):
        msgBuffer = Polynomial(list(message.coefficients))
        syndrome = self.syndrome(msgBuffer, errSize)
        cond = True
        for i in syndrome.coefficients:
            if i != GF256int(0) : cond = False
        
        if cond :
            print("pas d'erreurs")
            return msgBuffer[errSize:] # Change this if you want to return an error if it is not possible to restore the message
        
        errLoc = self.errorLocator(syndrome)

        errPos = self.errorPosition(errLoc)     

        if errLoc.len()-1 != len(errPos): return msgBuffer[errSize:] # Change this if you want to return an error if it is not possible to restore the message
        errorPolynome = self.errorPolynomial(syndrome,errLoc,errPos) 
        

        return (msgBuffer + errorPolynome)[errSize:]
        

