class GF2:

    def __init__(self,value):
        self.value = value

    def __one__(self):
        return GF2(1)
    
    def __zero__(self):
        return GF2(0)

    def __add__(self,other):
        return GF2(self.value ^ other.value)
    
    __sub__ = __add__
    __radd__ = __add__
    __rsub__ = __add__

    def __neg__(self):
        return self
    
    def __mul__(a,b):
        if a == GF2(0) or b ==  GF2(0):
            return  GF2(0)
        return GF2(1)
    
    def __pow__(self,power):
        return  self

    def inverse(self):
        return self

    def __div__(self,other):
        if other.value == 0 :
            raise ZeroDivisionError
        else : return self
    
    __truediv__ = __div__


    def _rdiv__(self,other):
        return self.inverse()* other
    
    def __repr__(self):
        return f"GF2({self.value})"

    def __str__(self):
        return f"sGF2({self.value})"

    def __eq__(self, other):
        return self.value == other.value
    
    def __neq__(self,other):
        return self.value != other.value
