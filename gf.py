from gf2 import GF2
from polynome import Polynomial
from primitivePolynomial import get_conway_polynomial, is_irreductible, is_primitive

def polynome_to_int(p:Polynomial):
    a = 0
    for i in range(p.len()-1,-1,-1):
        print(i)
        a = a*2 + p[i].value
    return a




class GF(type):
    def __new__(cls,element=2,pow=8, primitive = None):
        if element == 2 and pow == 8 : return GF2
        return super().__new__(cls)
    
    _GFEXP = []
	
    _GFLOG = []

    def __init__(self,element=2,pow=8, primitive = None):
        if element != 2 : raise NotImplemented
        
        self.characteristic = element ** pow
        self.element = element
        self.pow = pow

        if isinstance(primitive, Polynomial) and is_irreductible(primitive, pow) and is_primitive(primitive, pow) :
            self.int_primitive = polynome_to_int(primitive)
        elif isinstance(primitive, int):
            self.int_primitive = primitive
        else :
            self.int_primitive = polynome_to_int(get_conway_polynomial(pow))
    
        self._GFEXP = [0] * (self.characteristic * 2)
        self._GFLOG = [0] * self.characteristic

        self._GFEXP[0] = 1
        byteValu = 1

        for i in range(1,self.characteristic -1):
            byteValu <<= 1
            if (byteValu & self.characteristic):
                byteValu ^= self.int_primitive
			
            self._GFEXP[i] = byteValu
            self._GFLOG[byteValu] = i

        for i in range(self.characteristic -1 ,self.characteristic * 2):
            self._GFEXP[i] = self._GFEXP[i - (self.characteristic -1)]
        