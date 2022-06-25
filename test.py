import imp
import random
from gf256int import GF256int
from polynome import Polynomial
from rs import ReedSolomon
from polynomeGF import Message

message = "Hello, World"
error_size = 20
# Generate the necessary object for encode
rs = ReedSolomon(len(message)+error_size,len(message))

encoded = rs.encode(message)
encodederr = Polynomial(list(encoded.coefficients))
print("Message : ",encoded )

# Add error on the text
encodederr[30] = GF256int(111)
# Add error on the control sequence
encodederr[2] = GF256int(225)

print("Message with error : \n",Message.string(encodederr[error_size:]) )

# Décodage
decoded = rs.decode(encodederr,error_size)
print("Decoded Message : ", Message.string(decoded))


print("Message reconstructs ?",encoded[error_size:] == decoded)
