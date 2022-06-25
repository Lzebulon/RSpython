from gf256 import *

class GF256int(GF256):

    def __init__(self,value):
        self.value = value

    def __zero__(self):
        return GF256int(0)
    
    def __one__(self):
        return GF256int(1)

    def __add__(self,other):
        return GF256int(self.value ^ other.value)
    
    __sub__ = __add__
    __radd__ = __add__
    __rsub__ = __add__

    def __neg__(self):
        return self
    
    def __mul__(a,b):
        if a.value == 0 or b.value == 0:
            return GF256int(0)
        return GF256int(GF256int._GFEXP[ ( GF256int._GFLOG[a.value] + GF256int._GFLOG[b.value] ) % 255 ])
    
    def __pow__(self,power):
        return GF256int(GF256int._GFEXP[ (GF256int._GFLOG[self.value]*power) % 255])

    def inverse(self):
        return GF256int(GF256int._GFEXP[255 - GF256int._GFLOG[self.value]])

    def __div__(self,other):
        return self * other.inverse()
    
    __truediv__ = __div__

    def _rdiv__(self,other):
        return self.inverse()* other
    
    def __repr__(self):
        return f"GF256({self.value})"

    def __str__(self):
        return f"sGF256({self.value})"

    def __eq__(self, other):
        return self.value == other.value
    def __neq__(self,other):
        return self.value != other.value
