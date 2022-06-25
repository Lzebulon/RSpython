

class GF256:
    _GFEXP = [0] * 512
	
    _GFLOG = [0] * 256
    def __init__(self,element=2,pow=8):
        if element != 2 or pow != 8 : raise NotImplemented
        
        self._GFEXP[0] = 1
        byteValu = 1
        for i in range(1,255):
            byteValu <<= 1
            if (byteValu & 0x100):
                byteValu ^= 0x11d
			
            self._GFEXP[i] = byteValu
            self._GFLOG[byteValu] = i

        for i in range(255,512):
            self._GFEXP[i] = self._GFEXP[i - 255]
        
