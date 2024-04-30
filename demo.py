import streamlit as st
from compression import LZW
from compression import Metrics
from compression import RLE
from compression import Huffman
from compression import Golomb
from compression import Arithmetic

st.title("Data Compression Project")
text = st.text_input('Text to encode', 'abbfcsdfdddfadfafafa')
no_bitsBefore = len(text) * 8
st.write('Bits before encoding: ', no_bitsBefore)
H, prob = Metrics.entropy(text)
st.write('Entropy: ', H)
st.write('Probability occurence:', prob) # probability occurence

def printResults(before, after, encoded, isArithmetic = False):
    if isArithmetic:
        st.write('Encoded value:', encoded)
    else:
        if isinstance(encoded, float):
            # Format the float to three decimal places
            encoded_str = "%.3f" % encoded
        else:
            # Otherwise, keep the original encoded value
            encoded_str = str(encoded)
        st.write('Encoded value:', encoded_str)
    
    st.write('Bits after encoding: ', after)
    numerator, denominator = (before / after).as_integer_ratio()

    if(numerator > 1000):
        st.markdown('<center>Compression ratio</center>', unsafe_allow_html=True)

        # Convert before/after to a decimal and format it as a string
        compression_ratio = before / after
        latex_expression = f'{compression_ratio:.2f}'

        # Write the LaTeX expression using st.latex()
        st.latex(latex_expression)


    else:
        # Format the compression ratio as a LaTeX fraction
        latex_fraction = r'\frac{' + str(numerator) + '}{' + str(denominator) + '}'
        compression_ratio = before / after
        latex_expression = f'{compression_ratio:.2f}'

        # Write the compression ratio using LaTeX formatting
        st.markdown('<center>Compression ratio</center>', unsafe_allow_html=True)
        st.latex(latex_fraction)
        st.latex(latex_expression)

st.header('LZW')
lzw = LZW()
encoded_file = lzw.LZW_encoder(text)
bins = Metrics.binarify(encoded_file)
l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins))
before,after = Metrics.No_bits(text,bits_array=bins)
printResults(before, after, encoded_file)
st.write('Encoded file:', encoded_file)
st.write('bins: ', bins)
st.write('Average length: ', l_avg)
efficiency = H/l_avg * 100
f_efficiency = "{:.2f}".format(efficiency)
st.write('Efficiency: ', f_efficiency, '%')


st.header("Huffman")
huffman = Huffman()
encoded,d = huffman.encode(text)
after = len(encoded)
printResults(no_bitsBefore, after, encoded)
st.write('Key-value map: ', d)

avg_length = 0
for char, code in d.items():
    p = prob[char]
    avg_length += len(code) * p

st.write("Average length:", avg_length)
efficiency = H/avg_length * 100
f_efficiency = "{:.2f}".format(efficiency)
st.write('Efficiency: ', f_efficiency, '%')



# st.header('RLE')
# rle = RLE()
# encoded_file = rle.run_length_encoding(text)
# # bins = Metrics.binarify(encoded_file)
# # l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins))
# before, after = Metrics.No_bits(text, encoded_file)
# printResults(before, after, encoded_file)
# # st.write('Length average: ', l_avg)