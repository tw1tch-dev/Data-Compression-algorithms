import streamlit as st
from compression import LZW
from compression import Metrics
from compression import RLE
from compression import Huffman
from compression import Golomb
from compression import Arithmetic

with open('css/styles.css', 'r') as file:
    css = file.read()

st.markdown(f"""
    <style>
        {css}
    </style>
""", unsafe_allow_html=True)

# title
st.title("Data Compression Project")

# popover for instructions
with st.popover("Usage instructions"):
    st.markdown("Hello there! 👋  \n\nIn order to use Golomb Code, you need to put digits only and separated by commas (,).     \n Example: 2,5,1500,3,3,2")

# text to encode
text = st.text_input('Text to encode', 'abbfcsdfdddfadfafafa')

golombOnly = False # check whether to use golomb only or everything else
if not text:
    st.warning("Text input is empty. Please enter text to use the encoding algorithms.")
    st.stop()
elif text.replace(',', '').isdigit():
    golombOnly = True
    parts = text.split(',')

no_bitsBefore = len(text) * 8
st.write('Bits before encoding: ', no_bitsBefore)
H, prob = Metrics.entropy(text)
st.write('Entropy: ', H)
# st.write('Probability occurence:', prob) # probability occurence

formatted_string = "| Character | Probability |\n| ----------- | ----------- |\n"

for letter, probability in prob.items():
    formatted_string += f"| {letter} | {round(probability, 2)} |\n"

st.markdown(formatted_string)
st.markdown("----")

def printResults(before, after, encoded, isArithmetic = False):
    if isArithmetic:
        if isinstance(encoded, float):
            # Format the float to remove trailing zeros
            encoded_str = "{:.6f}".format(encoded).rstrip('0').rstrip('.')
        else:
            # Otherwise, keep the original encoded value
            encoded_str = str(encoded)
        st.write('Encoded value:', encoded_str)

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

if not golombOnly:
    # LZW
    st.header('LZW')
    lzw = LZW()
    encoded_file = lzw.LZW_encoder(text)
    bins = Metrics.binarify(encoded_file)
    l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins))
    before,after = Metrics.No_bits(text,bits_array=bins)
    printResults(before, after, encoded_file)
    st.write('Average length: ', l_avg)
    efficiency = H/l_avg * 100
    f_efficiency = "{:.2f}".format(efficiency)
    st.write('Efficiency: ', f_efficiency, '%')
    st.markdown("----")

    # Huffman
    st.header("Huffman")
    huffman = Huffman()
    encoded, d = huffman.encode(text)
    after = len(encoded)
    printResults(no_bitsBefore, after, encoded)
    formatted_string = "| Letter | Codeword |\n| ----------- | ----------- |\n"

    for letter, codeword in d.items():
        formatted_string += f"| {letter} | {codeword} |\n"

    st.markdown(formatted_string)

    avg_length = 0
    for char, code in d.items():
        p = prob[char]
        avg_length += len(code) * p

    st.write("Average length:", avg_length)
    efficiency = H/avg_length * 100
    f_efficiency = "{:.2f}".format(efficiency)
    st.write('Efficiency: ', f_efficiency, '%')
    st.markdown("----")


    # RLE
    st.header('RLE')
    rle = RLE()
    encoded_file = rle.run_length_encoding(text)
    before, after = Metrics.No_bits(text, encoded_file)
    printResults(before, after, encoded_file)
    st.markdown("----")

    # Arithmetic
    st.header('Arithmetic')
    H, table = Metrics.entropy(text)
    symbols = list(table.keys())
    probabilities = [round(prob, 2) for prob in table.values()]
    sorted_symbols, sorted_probabilities = zip(*sorted(zip(symbols, probabilities)))
    sequence = st.text_input('Sequence') # needs revision
    if not sequence:
        st.warning("You need to put in the sequence.")
        st.stop()
    encoded_value = Arithmetic.encode_sequence(sequence, sorted_symbols, sorted_probabilities)      

    binary_encoded_value = bin(int(encoded_value * (2 ** 64)))[2:]
    num_bits_after = len(binary_encoded_value)

    printResults(no_bitsBefore, num_bits_after, encoded_value, isArithmetic = True)
    st.markdown("----")

# GOLOMB ONLY WORKS WITH INTEGERS
if golombOnly:
    st.header('Golomb')
    golomb = Golomb()
    encoded_file = []
    num_list = []
    m = 1000
    parts = text.split(',')
    for part in parts:
        num = int(part)
        num_list.append(num)

    if num_list:
        max_num = max(num_list)
        m = 2 ** (max_num.bit_length())

    m_input = st.text_input('M value', m)
    m = int(m_input)
    if num_list:
        for num in num_list:
            encoded_file.append(golomb.golomb_encode(num, m))
    bins = Metrics.binarify(num_list)
    before  = len(bins) * len(bins[0])
    _,after = Metrics.No_bits("",bits_array=encoded_file)
    st.write('Bits before encoding: ', before)
    printResults(before, after, encoded_file)