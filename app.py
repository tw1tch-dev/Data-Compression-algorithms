import streamlit as st
from compression import LZW
from compression import Metrics
from compression import RLE
from compression import Huffman
from compression import Golomb
from compression import Arithmetic

st.markdown("""
<style>
.st-emotion-cache-ot9ait {
    visibility:hidden;
}
h2 {
    border-left-style: solid;
    border-left-color: gray;
    padding-left: 15px;
    border-bottom-style: solid;
    border-bottom-color: gray;
}
</style>""", unsafe_allow_html=True)

st.title("Data Compression Project")
text = st.text_input('Text to encode', 'abbfcsdfdddfadfafafa')
no_bitsBefore = len(text) * 8
st.write('Bits before encoding: ', no_bitsBefore)
# st.write('Text to be encoded is ', text)
# if before / after as integer ratio is so big then print before/after
# return compressionRatio for comparison
def printResults(before, after):
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

col1, col2, col3 = st.columns(3)

with col1:
    st.header("RLE")
    rle = RLE()
    encoded_file = rle.run_length_encoding(text)
    # st.write("Encoded value: ", encoded_file)
    before,after = Metrics.No_bits(text,encoded_file)

    printResults(before, after)
    # st.markdown('<center>Compression ratio</center>', unsafe_allow_html=True)
    # st.markdown('<center>' + str(before/after) +'</center>', unsafe_allow_html=True)

with col2:
    st.header("Huffman")
    huffman = Huffman()
    encoded,d = huffman.encode(text)
    after = len(encoded)
    printResults(no_bitsBefore, after)

with col3:
    # revise sequence stuff
    st.header("Arithmetic")
    H,table = Metrics.entropy(text)
    symbols = table.keys()
    probabilities = table.values()

    sequence = "abc"
    # Encode the sequence
    encoded_value = Arithmetic.encode_sequence(sequence, symbols, probabilities)
    # bins = Metrics.binarify(encoded_value)
    # before,after = Metrics.No_bits(text,bits_array=bins)
    # printResults(before, after)
    # Output the encoded value
    # st.write("Encoded value:", encoded_value)
    # Convert the decimal value to its binary representation
    binary_representation = format(encoded_value, '.50f')
    # Count the number of bits required to represent the binary number (excluding the '0.' part)
    num_bits = len(binary_representation) - 2

    printResults(no_bitsBefore, num_bits)
    # compression_ratio = no_bitsBefore / encoded_value
    # st.write("Compression ratio:", compression_ratio)

st.markdown("----")
col4, col5 = st.columns(2)
    
with col4:
    st.header("Golomb")
    
    golomb = Golomb()
    encoded_file = []
    m = 1000
    for integer in text:
        encoded_file.append(Golomb.golomb_encode(ord(integer),m))
    
    n_bits_before, n_bits_after = Metrics.No_bits(text, None, encoded_file)
    printResults(n_bits_before, n_bits_after)

with col5:
    st.header("LZW")
    lzw = LZW()
    encoded_file = lzw.LZW_encoder(text)
    bins = Metrics.binarify(encoded_file)
    l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins))
    H,d= Metrics.entropy(text)
    before,after = Metrics.No_bits(text,bits_array=bins)
    printResults(before, after)
    # st.write('Bits after encoding: ', after)
    # numerator, denominator = (before / after).as_integer_ratio()

    # # Format the compression ratio as a LaTeX fraction
    # latex_fraction = r'\frac{' + str(numerator) + '}{' + str(denominator) + '}'

    # # Write the compression ratio using LaTeX formatting
    # st.markdown('<center>Compression ratio</center>', unsafe_allow_html=True)
    # st.latex(latex_fraction)

st.markdown("----")

# this is here for the idea of compression ratio
# st.metric(label='Ratio', value = '72%', delta = '+1.27%')