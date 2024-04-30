
import math
import numpy as np
class Golomb:
    def __init__(self,):
        pass
    
    @staticmethod
    def golomb_encode(value, m):
        # Calculate the quotient and remainder
        quotient = value // m
        remainder = value % m
        
        # Generate the unary code
        unary_code = "1" * quotient + "0"
        d          = 2**math.ceil(math.log2(m)) - m
        if remainder < d:
            n_bits    = int(math.floor(math.log2(m)))
        else:
            n_bits    = int(math.ceil(math.log2(m)))
            remainder = remainder + d 
        # Generate the binary code with a fixed length determined by the number of bits required to represent m - 1
        binary_code = format(remainder, "0" + str(n_bits) + "b")
        
        # Combine the unary and binary codes to form the encoded value
        return unary_code + binary_code
    @staticmethod
    def golomb_decode(encoded_value, m):
        # Find the length of the unary code by locating the first '0' in the encoded value
        unary_code_length = encoded_value.index("0") + 1
        
        # Calculate the quotient based on the length of the unary code
        quotient = unary_code_length - 1
        
        # Extract the binary code from the encoded value using the length of the unary code and the number of bits required to represent m - 1
        binary_code = encoded_value[unary_code_length:unary_code_length + m.bit_length() - 1]
        
        # Convert the binary code to an integer to obtain the remainder
        remainder = int(binary_code, 2)
        
        # Calculate the decoded value by multiplying the quotient by m and adding the remainder
        return quotient * m + remainder
