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

ratio = []
def compareAlgorithms(ratio):
    # Initialize formatted string
    formatted_string = "| Algorithm | Compression Ratio |\n| ----------- | ----------- |\n"

    # Iterate over each algorithm and its compression ratio
    for algo, value in ratio:
        # Append row to the formatted string
        if value == max(ratio, key=lambda x: x[1])[1]:
            # Highlight the maximum compression ratio row in green and bold
            formatted_string += f"| <span style='color:#00C11A; font-weight:bold; font-style:italic;'>{algo}</span> | <span style='color:#00C11A; font-weight:bold; font-style:italic;'>{round(value, 2)}</span> |\n"
        else:
            # Regular row
            formatted_string += f"| {algo} | {round(value, 2)} |\n"

    # Render the formatted string using markdown
    st.markdown(formatted_string, unsafe_allow_html=True)
    
    # Find the algorithm with the highest compression ratio
    best_algorithm = max(ratio, key=lambda x: x[1])
    
    # Return the name of the best algorithm
    return best_algorithm[0]



golombOnly = False # boolean to check whether to use golomb only or everything else

# warning message if there is no input
if not text:
    st.warning("Text input is empty. Please enter text to use the encoding algorithms.")
    st.stop()
elif text.replace(',', '').isdigit(): # check if input is digits only and separated by commas or not
    golombOnly = True
    parts = text.split(',')

# Entropy and probability are global too, they don't depend on a particular algorithm
H, prob = Metrics.entropy(text, True)
# bits before encoding is global so print it before any other algorithm
if not golombOnly:
    no_bitsBefore = len(text) * 8
    st.write('Bits before encoding: ', no_bitsBefore)
    H, prob = Metrics.entropy(text)
st.write('Entropy: ', H)

formatted_string = "| Character | Probability |\n| ----------- | ----------- |\n"

for letter, probability in prob.items():
    formatted_string += f"| {letter} | {round(probability, 2)} |\n"

st.markdown(formatted_string)
st.markdown("----")

if not golombOnly:
    # LZW
    st.header('LZW')

    lzw = LZW()
    encoded_file = lzw.LZW_encoder(text)
    bins = Metrics.binarify(encoded_file) # turn integers to their binary representation
    l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins)) # calc average length
    before,after = Metrics.No_bits(text,bits_array=bins) # calc no. of bits before and after encoding

    ratio.append(('LZW', before/after))

    Metrics.printResults(before, after, encoded_file)

    st.write('Average length: ', l_avg)

    # efficiency
    efficiency = H/l_avg * 100
    f_efficiency = "{:.2f}".format(efficiency)
    st.write('Efficiency: ', f_efficiency, '%')

    st.markdown("----")

    # Huffman
    st.header("Huffman")
    huffman = Huffman()
    encoded, d = huffman.encode(text)
    after = len(encoded)

    Metrics.printResults(no_bitsBefore, after, encoded)

    ratio.append(('Huffman', no_bitsBefore/after))

    # table for the codewords
    formatted_string = "| Letter | Codeword |\n| ----------- | ----------- |\n"
    for letter, codeword in d.items():
        formatted_string += f"| {letter} | {codeword} |\n"

    st.markdown(formatted_string)

    # calculate average length
    avg_length = 0
    for char, code in d.items():
        p = prob[char]
        avg_length += len(code) * p

    st.write("Average length:", avg_length)

    # efficiency
    efficiency = H/avg_length * 100
    f_efficiency = "{:.2f}".format(efficiency)
    st.write('Efficiency: ', f_efficiency, '%')
    st.markdown("----")


    # RLE
    st.header('RLE')

    rle = RLE()
    encoded_file = rle.run_length_encoding(text)
    before, after = Metrics.No_bits(text, encoded_file)

    Metrics.printResults(before, after, encoded_file)

    ratio.append(('RLE', before/after))

    st.markdown("----")

    # Arithmetic
    st.header('Arithmetic')

    H, table = Metrics.entropy(text)
    symbols = list(table.keys())
    probabilities = [round(prob, 2) for prob in table.values()]

    sorted_symbols, sorted_probabilities = zip(*sorted(zip(symbols, probabilities)))

    sequence = st.text_input('Sequence')
    # if user didn't put in a sequence, show the warning
    if not sequence:
        st.warning("You need to put in the sequence.")
        st.stop()
    
    # continue encoding with the sequence
    encoded_value = Arithmetic.encode_sequence(sequence, sorted_symbols, sorted_probabilities)

    # turn encoded value to binary representation to get bits after encoding
    binary_encoded_value = bin(int(encoded_value * (2 ** 64)))[2:]
    num_bits_after = len(binary_encoded_value)

    Metrics.printResults(no_bitsBefore, num_bits_after, encoded_value, isArithmetic = True)

    ratio.append(('Arithmetic', no_bitsBefore/num_bits_after))

    st.markdown("----")

# GOLOMB ONLY WORKS WITH INTEGERS
if golombOnly:
    st.header('Golomb')

    golomb = Golomb()
    encoded_file = []
    num_list = []
    m = 1000

    # splitting the input by commas
    parts = text.split(',')
    for part in parts:
        num = int(part)
        num_list.append(num)

    # choosing the best m value
    if num_list:
        max_num = max(num_list)
        m = 2 ** (max_num.bit_length())

    # user is given option to set custom m value
    m_input = st.text_input('M value', m)
    m = int(m_input)

    # encode again if user inputs a new m value
    if num_list:
        for num in num_list:
            encoded_file.append(golomb.golomb_encode(num, m))

    
    bins = Metrics.binarify(num_list) # turn integers to their binary representation
    before  = len(bins) * len(bins[0]) # calc bits before encoding
    _,after = Metrics.No_bits("",bits_array=encoded_file) # calc bits after encoding

    # output
    st.write('Bits before encoding: ', before)
    Metrics.printResults(before, after, encoded_file)

# NOW HERE I NEED TO CHOOSE THE BEST TECHNIQUE AFTER COMPARISON
if not golombOnly:
    st.write('Best algorithm is ', compareAlgorithms(ratio))