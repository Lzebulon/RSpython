from gf256int import GF256int


class Polynomial(object):
    def __init__(self,coefficients) :
        self.coefficients = coefficients if len(coefficients) > 0 else [GF256int(0)]
        self._n = len(coefficients)  

    def deg(self):
        self._trim_()
        self._n = len(self.coefficients)
        return self._n-1
    
    def len(self):
        return len(self.coefficients)

    def _zero_(self):
        return self.coefficients[0]-self.coefficients[0]
        

    def _trim_(self):
        zero = self._zero_()
        while self.len() > 1 and self.coefficients[-1]==zero:
            self.coefficients.pop()
            self._n -= 1


    def __add__(self,other):
        nsum = max(self._n,other._n)
        sum = [self._zero_()] * nsum

        for i in range(self.len() ):
            sum[i] = self.coefficients[i]
        
        for i in range(other.len() ):
            sum[i] += other.coefficients[i]
        
        return Polynomial(sum)
    

    def __getitem__(self,key):
        if isinstance(key, slice): return Polynomial(self.coefficients[key])
        if abs(key) >= self.len() : raise IndexError
        return self.coefficients[key]

    def __setitem__(self,key,value):
        if abs(key) >= self._n : raise IndexError
        self.coefficients[key] = value

    def __neg__(self):
        return Polynomial([-x for x in self.coefficients])
    
    def __one__(self):
        return self.coefficients[0].__one__()

    def __sub__(self,other) :
        return self + (-other)

    def __mul__(self,other):
        if isinstance(other,type(self.coefficients[0])): return Polynomial([x * other for x in self.coefficients ])
        if isinstance(other,Polynomial) : 
            nc = self._n + other._n - 1
            polyC = [self._zero_()] * nc
            for i in range(other._n):
                for j in range(self._n):
                    polyC[i+j] += other[i] * self[j]
            
            return Polynomial(polyC)
        else : raise NotImplemented

    def __str__(self) :
        return f"Polynome : {self.coefficients}"

    def __floordiv__(self, other):
        return divmod(self, other)[0]
    def __mod__(self, other):
        return divmod(self, other)[1]

    def __divmod__(self,other):
        remainder = Polynomial(self.coefficients)
        zero = self[0] - self[0]
        p_zero = Polynomial([zero])
        one = other.__one__()
        if other == Polynomial([one]):
            return (self, Polynomial([zero]))
        x = Polynomial([zero,one])
        quotient = Polynomial([zero])

        while remainder != p_zero and remainder.deg() >= other.deg():
            r_lead = remainder.coefficients[-1]
            o_lead = other.coefficients[-1]
            q_part = Polynomial([r_lead/o_lead])
            q_deg = remainder.deg()-other.deg()
            if q_deg > 0 :
                q_part *= Polynomial([zero for x in range(q_deg)]+[one])
            r_sub = other * q_part
            remainder -= r_sub
            quotient += q_part
        return (quotient,remainder)


    def __eq__(self, other):
        if self.deg() != other.deg():
            return False
        for i in range(self.len()):
            if self[i] != other[i]:
                return False
        return True
    
    def __ne__(self, other) -> bool:
        return not ( self == other )


    def __div__(self,other):
        div,mod = divmod(self,other)
        assert mod == Polynomial([self._zero_()])
        return div

    def __floordiv__(self,other):
        return divmod(self,other)[0]

    def __pow__(self,power):
        if power < 1 : return Polynomial([self.__one__()])
        elif power % 2 == 0: return (self*self) ** (power//2)
        else : return ((self*self) ** (power//2)) * self


    def evaluate(self,x):
        if not isinstance(x,type(self.coefficients[0])) : return NotImplementedError
        value = self.coefficients[-1]
        for i in range(self.len() - 2, -1, -1):
            value = value * x + self.coefficients[i]
        return value

    def derive(self):
        return Polynomial([GF256int(i+1) * self.coefficients[i] for i in range(1,self._n) ])
