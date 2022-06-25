from email import message
from gf256int import GF256int
from polynome import Polynomial


class Message():
    @staticmethod
    def int(p:Polynomial):
        return [x.value for x in p]
    

    
    @staticmethod
    def int_polynome(p:Polynomial):
        x = ""
        for i in range(p.len()):
            if p[i] != GF256int(0) :
                if x != "":
                    x += " + "
                x += f"{p[i].value} x^{i}"
        return x if x != "" else "0"
    
    @staticmethod
    def hex(p:Polynomial):
        x = ""
        for i in range(p.len()):
            x += f"{p[::-1][i].value:X} "
        return x if x != "" else "0"

    @staticmethod
    def GF256_polynome(p:Polynomial):
        x = ""
        for i in range(p.len()):
            if p[i] != GF256int(0) :
                if x != "":
                    x += " + "
                x += f"{p[i]} x^{i}"
        return x if x != "" else "GF256(0)"

    @staticmethod
    def string(p:Polynomial):
        l = [chr(x.value) for x in p][::-1]
        s = ""
        for x in l:
            s += x
        return s

    @staticmethod
    def bin_to_polynomial(p:list):
        message = []
        for i in range(0,len(p),8):
            message.append(GF256int(int("0b"+"".join(map(str,p[i:i+8])),base=0)))
        return Polynomial(message)

    @staticmethod
    def polynomial_to_bin(p:Polynomial):
        message = []
        for x in p:
            nombre = bin(x.value)[2:]
            nombre_decompo = [0]*(8-len(nombre))+[int(i) for i in nombre]
            message += nombre_decompo
        return message