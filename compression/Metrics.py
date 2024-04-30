
import math 
import re
class Metrics:
    def __init__(self):
        pass
    @staticmethod
    def binarify(encoded_file):
        """
        this function turns list of integers ito it's binary representation
        input:
        encoded_file(list)----> list of integers represent the compressed file
        output:
        bin_ints(list)--------> list of Strings of binary representation for each int
        """
        n_bits = int(math.ceil(math.log2(max(encoded_file)+1)))
        bin_ints = []
        for integer in encoded_file:
            bin_ints.append(format(int(integer),f"0{n_bits}b"))
        return bin_ints
    @staticmethod
    def Avg_length(bits_array, p_array):
        """
        calculate the average length Warning! " both inputs must have the same length with 
        the same order of appearance"
        inputs:
        bits_array(list)--------> array of bits that represent the compressed file
        p_array(list)-----------> array of probabilities of each character
        output:
        avg_length(integer)-----> average length value
        """
        l1 = bits_array
        l1 = [len(str(v)) for v in l1]
        l2 = p_array
        if len(l1) != len(l2) :
            raise Exception("Two arrays must have the same length")
        avg_length = sum([l*p for l,p in zip(l1,l2)])
        return avg_length
    @staticmethod
    def No_bits(file, encoded_file = None, bits_array = None):
        """
        calculate the number of bits before and after compression
        inputs:
        file(String)-------------> the original file 'before compression' 
        encoded_file(String)-----> the file after compression 'RLE'
        bits_array(list)---------> array of bits that represent the compressed file 'LZW-Huffman..etc'
        outputs:
        n_bits_before(integer)---> number of bits required before compression
        n_bits_after(integer)----> number of bits required after  compression
        """
        n_bits_before = len(file) * 8
        if bits_array == None:
            ints         = re.findall("\d+",encoded_file)
            ints         = [int(i) for i in ints]
            strings      = re.split("\d+|\s",encoded_file)
            strings.remove("")
            n_bits_after = (len(strings) * 8) + (len(ints) * math.ceil(math.log2(max(ints)+1)))
        else:
            n_bits_after = sum([len(bits) for bits in bits_array])
        return n_bits_before,n_bits_after
    @staticmethod
    def entropy(file):
        """
        caculate the entropy and alphabet distribution
        input:
        file(String)-------> original file 
        outputs:
        warning! 'outputs in tuple of size two'
        H(float)-----------> claude shannon entropy 
        alpha_dist(dict)---> distribution of each character in the file
        """
        alpha_dist = dict()
        n = len(file)
        for c in file:
            if c in alpha_dist:
                alpha_dist[c] += 1/n
            else:
                alpha_dist[c] = 1/n
        H = 0
        for p in alpha_dist.values(): 
            H += p * math.log2(1/p)
        return H,alpha_dist
    
    
