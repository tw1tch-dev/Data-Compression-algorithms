import streamlit as st
import random
import math

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

mainTab, instructionsTab = st.tabs(["Program", "Instructions"])

with instructionsTab:
    st.subheader('Instructions')
    st.markdown("Hello there! 👋  \n\nIn order to use Golomb Code, you need to put digits only and separated by commas (,).     \n \u2022 Example: 2,5,1500,3,3,2")
    st.markdown('----')
    
    st.subheader('How is everything calculated?')
    st.latex(r'E = -\sum_{i} p_i \log_2(p_i)')
    st.latex(r'L_{\text{av}} = \sum_i L_i \ p_i')
    st.latex(r'Efficiency = \frac{E}{L_{\text{av}}} \times 100')
    st.markdown('----')

with mainTab:
    # text to encode
    text = st.text_input('Text to encode', 'abbfcsdfdddfadfafafa')

    # variables declaration
    no_bitsBefore = len(text) * 8
    ratio = []
    RLEavailable = False

    # FUNCTIONS
    def compareAlgorithms(ratio):
        st.subheader('Techniques Comparison')
        formatted_string = "| Technique | Compression Ratio |\n| ----------- | ----------- |\n"

        for algo, value in ratio:
            if value == max(ratio, key=lambda x: x[1])[1]:
                # if it's the highest CR, then highlight it
                formatted_string += f"| <span style='color:#00C11A; font-weight:bold; font-style:italic;'>{algo}</span> | <span style='color:#00C11A; font-weight:bold; font-style:italic;'>{round(value, 2)}</span> |\n"
            else:
                formatted_string += f"| {algo} | {round(value, 2)} |\n"

        # print the comparison in table
        st.markdown(formatted_string, unsafe_allow_html=True)
        st.write('\n')
        
        # find the algorithm with the highest compression ratio
        best_algorithm = max(ratio, key=lambda x: x[1])
        
        # return the name of the best algorithm
        return best_algorithm[0]

    # check if the text is binary
    def is_binary(text):
        return all(char in '01' for char in text)

    # check if the text is binary AND without commas (to use Golomb + RLE)
    def is_binary_without_commas(text):
        return all(char in '01' for char in text) and ',' not in text

    # check if the text has integers to encode using Golomb
    def is_integer_sequence(text):
        parts = text.split(',')
        return all(part.isdigit() for part in parts)

    # generates a test sequence for the arithmetic encoding (can be changed manually by user)
    def generate_test_sequence(text, symbols, probabilities):
        cumulative_probabilities = [0]
        for prob in probabilities:
            cumulative_probabilities.append(cumulative_probabilities[-1] + prob)

        test_sequence = []
        for _ in range(len(text)):
            rand_num = random.random()
            for i, cumulative_prob in enumerate(cumulative_probabilities):
                if rand_num < cumulative_prob:
                    test_sequence.append(symbols[i - 1])
                    break

        return ''.join(test_sequence)


    # if the text is integers, then we can use golomb only
    if is_integer_sequence(text):
        golombOnly = True
        parts = text.split(',')
        # if the text is binary number without commas then can use RLE technique too
        if is_binary_without_commas(text):
            RLEavailable = True
    else:
        golombOnly = False

    if text:
        if not golombOnly:
            st.write('Bits before encoding: ', no_bitsBefore)
            H, prob = Metrics.entropy(text)
        else:
            # here metrics entropy has true argument so when counting the bits of text, it doesnt count the commas
            H, prob = Metrics.entropy(text, True)
        st.write('Entropy: ', round(H, 2))

    # check if input text is empty
    if not text:
        st.warning("Text input is empty. Please enter text to use the encoding algorithms.")
        st.stop()

    # now begin using the techniques based on the previous if statements and depending on text input type
    elif golombOnly:
        # if the input is binary number and has no commas then can use RLE
        if RLEavailable:
            st.header('RLE')

            rle = RLE()
            encoded_file, vectorsNum, maxNum = rle.run_length_encoding(text)
            before, after = Metrics.No_bits(text, encoded_file)
            # if text is binary, calculate 'after' like we learnt in the lecture
            # rule: no. of vectors * (bits the encoded char/num takes + log2 of [the maximum number + 1])
            if is_binary(text):
                before = len(text)
                after = (vectorsNum) * (1 + math.ceil(math.log2(maxNum+1)))

            Metrics.printResults(before, after, encoded_file)

            ratio.append(('RLE', before/after))

            st.markdown("----")

        # Golomb encoding
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

        if is_binary(text): # check if it will count commas too
            before = len(text)

        # output
        st.write('Bits before encoding: ', before)
        Metrics.printResults(before, after, encoded_file)
        ratio.append(('Golomb', before/after))
        st.markdown("----")

    else:
        # LZW
        st.header('LZW')

        lzw = LZW()
        encoded_file = lzw.LZW_encoder(text)
        bins = Metrics.binarify(encoded_file)
        l_avg = Metrics.Avg_length(bins, [1/len(bins)]*len(bins))
        before, after = Metrics.No_bits(text, bits_array=bins)

        Metrics.printResults(before, after, encoded_file)

        ratio.append(('LZW', before/after))

        st.write('Average length: ', round(l_avg, 2))

        # efficiency calculation
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

        st.write("Average length:", round(avg_length, 2))

        # efficiency
        efficiency = H/avg_length * 100
        f_efficiency = "{:.2f}".format(efficiency)
        st.write('Efficiency: ', f_efficiency, '%')
        st.markdown("----")

        # RLE
        st.header('RLE')

        rle = RLE()
        encoded_file, vectorsNum, maxNum = rle.run_length_encoding(text)
        before, after = Metrics.No_bits(text, encoded_file)
        if is_binary(text):
            before = len(text)
            after = (vectorsNum) * (1 + math.ceil(math.log2(maxNum+1)))

        Metrics.printResults(before, after, encoded_file)

        ratio.append(('RLE', before/after))

        st.markdown("----")

        # Arithmetic

        # section examples, each text is generated to match with the probabilities of the section problems
        # text: cbaaaaaaaacaaaaccacaaacaaaaaacaaccaaaaaaccaabcaaaaaacaaaaaaaaacaccccaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # seq: acba

        # text: bcbabcbabc
        # seq: bac

        st.header('Arithmetic')

        H, table = Metrics.entropy(text)
        symbols = list(table.keys())
        probabilities = [round(prob, 2) for prob in table.values()]
        
        # final check for probabilities if it doesn't sum up to 1, mainly to prevent errors
        sum_probabilities = sum(probabilities)
        if sum_probabilities != 1.0:
            probabilities = [prob / sum_probabilities for prob in probabilities]
        
        # sorting the symbols/probabilities to prepare for arithmetic encoding
        sorted_symbols, sorted_probabilities = zip(*sorted(zip(symbols, probabilities)))

        # give the user an option to put his sequence
        sequence_input = st.text_input('Sequence')

        if sequence_input:
            sequence = sequence_input
        else:
            # if the sequence input is empty then generate a test sequence using a function defined above
            sequence = generate_test_sequence(text, symbols, probabilities)
            st.write('Current generated sequence: ', sequence)

        # continue encoding with the sequence
        encoded_value = Arithmetic.encode_sequence(sequence, sorted_symbols, sorted_probabilities)

        # turn encoded value to binary representation to get bits after encoding
        binary_encoded_value = bin(int(encoded_value * (2 ** 64)))[2:]
        num_bits_after = len(binary_encoded_value)

        Metrics.printResults(no_bitsBefore, num_bits_after, encoded_value, isArithmetic=True)
        ratio.append(('Arithmetic', no_bitsBefore/num_bits_after))

        st.markdown("----")

    # Display the best technique
    count = 0
    for algo, value in ratio:
        count += 1

    if count != 1:
        st.markdown('\u2022 The most optimal technique is **' + compareAlgorithms(ratio) + '**.', unsafe_allow_html=True)
    
    # TODO make a checkbox for algorithms to use maybe, check more for input errors and different algorithms
        