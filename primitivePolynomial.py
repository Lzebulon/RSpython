from gf2 import GF2
from polynome import *


def cherche_pivot(m,i,r):
    it = r
    for j in range(r+1,len(m)):
        if m[j][i] != GF2(0) and m[it][i] == GF2(0):
            it = j
    return it

def echange(m,i,j):
    m[j], m[i] = m[i], m[j]

def transvection(m, i, r, a):
    for j in range(len(m)):
        m[i][j] -= a * m[r][j]
    
def pivot(m):
    r = -1
    for j in range(0,len(m)):

        k = cherche_pivot(m,j,r+1)

        if m[k][j] != GF2(0):
            r += 1
            echange(m,k,r)

            for i in range(0,len(m)):
                if i!= r:
                    transvection(m,i,r,m[i][j])
    return r+1,m

def calcul_sp(P:Polynomial,n):
    base = [[GF2(0) for i in range(n)] for j in range(n)]
    for i in range(n):
        Q = Polynomial([GF2(0) for j in range(2*i)] + [GF2(1)]) # Q = X^{i*n}
        QmodP = (Q % P)
        for j in range(n):
            if j < QmodP.len():
                base[i][j] = QmodP.coefficients[j] 
        base[i][i] -= GF2(1)
    return base

def is_irreductible(P,n):
    return P.deg() - pivot(calcul_sp(P,n))[0] == 1

def is_primitive(P,n):
    nb = 2**n -1
    j = 0
    while  j < nb and not (Polynomial([GF2(1) for t in range(1) if j > 0]+[GF2(0) for i in range(1,j)]+[GF2(1)]) % P == Polynomial([GF2(0)])):
        j += 1
    return j == nb and (Polynomial([GF2(1)]+[GF2(0) for i in range(1,j)]+[GF2(1)]) % P == Polynomial([GF2(0)]))
    


def get_primitive_polynomial(n):
    p = Polynomial([GF2(1)]+[GF2(0) for i in range(1,n)]+[GF2(1)])
    j = 0
    l = []
    if (is_irreductible(p,n) and is_primitive(p,n)): l.append(p)
    while p.coefficients != [GF2(1)]*(n+1) :
        j+=1
        r = []
        c = False
        b = True
        for i in range(1,p.len()-1):
            a = p[i] == GF2(1)
            unite = (a and not(b) and not(c)) or\
                (not(a) and b and not(c)) or\
                (not(a) and not(b) and c) or\
                (a and b and c)
            
            if unite :
                r =  r + [GF2(1)]
            else : r =  r + [GF2(0)]
            c = (a and b) or (b and c) or (a and c)

            b = False
        r = [GF2(1)]+r+[GF2(1)]
        p = Polynomial(r)
        if (is_irreductible(p,n) and is_primitive(p,n)): l.append(p.coefficients)
    return l

def get_proper_divisor(n):
    return [x for x in range(1,(n+1)//2 +1) if n%x == 0 and n != x]

def is_conway_polynomial(p,n,conway_polynomial_proper_divisor):
    nb = 2**n -1
    for c in conway_polynomial_proper_divisor :
        nc = 2**(c.deg()) - 1
        k = nb//nc
        pc = Polynomial([GF2(0) for _ in range(c.len()*k)])
        for i in range(c.len()):
            pc[i*k] = c[i]
        if (pc % p) != Polynomial([GF2(0)]) : return False
    return True

def get_conway_polynomial(n, conway_polynomial_divisor = []):
    p = Polynomial([GF2(1)]+[GF2(0) for i in range(1,n)]+[GF2(1)])
    j = 0
    if conway_polynomial_divisor == [] :
        proper_divisor = get_proper_divisor(n)
        conway_polynomial_proper_divisor = [] 
        for pol in proper_divisor :
            conway_polynomial_proper_divisor.append(get_conway_polynomial(pol,conway_polynomial_proper_divisor))
    else :
        print(conway_polynomial_divisor)
        conway_polynomial_proper_divisor = [cp for cp in conway_polynomial_divisor if n % cp.deg() == 0]

    while not (is_irreductible(p,n) and is_primitive(p,n) and is_conway_polynomial(p,n,conway_polynomial_proper_divisor)) :
        if p.coefficients == [GF2(1)]*(n+1) : raise Exception("Aucun polynome de conway trouvé")
        j+=1
        print(j,2**n)
        r = []
        c = False
        b = True
        for i in range(1,p.len()-1):
            a = p[i] == GF2(1)
            unite = (a and not(b) and not(c)) or\
                (not(a) and b and not(c)) or\
                (not(a) and not(b) and c) or\
                (a and b and c)
            
            if unite :
                r =  r + [GF2(1)]
            else : r =  r + [GF2(0)]
            c = (a and b) or (b and c) or (a and c)
            b = False

        r = [GF2(1)]+r+[GF2(1)]
        p = Polynomial(r)
    return p
