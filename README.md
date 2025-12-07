# Data Compression Algorithms Comparison Web App  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

An interactive **Streamlit web application** that lets you compare **5 classic lossless data compression algorithms** side-by-side on your own input text:

| Algorithm         | Type                     | Best For                                      |
|-------------------|--------------------------|-----------------------------------------------|
| **RLE**           | Run-Length Encoding      | Long runs of identical symbols (e.g. binary)  |
| **Huffman Coding**| Variable-length prefix    | General text with uneven symbol distribution  |
| **Golomb Coding** | Parameterized prefix     | Non-negative integers (geometric distribution)|
| **Arithmetic Coding** | Fractional encoding  | Near-optimal, approaches Shannon entropy      |
| **LZW**           | Dictionary-based         | Text with repeating phrases (e.g. English)    |

## Features

- Automatic detection of input type (text, binary, integer sequences)
- Smart algorithm availability:
  - Golomb → only for comma-separated positive integers
  - RLE → enhanced for binary strings & integer runs
- Calculates:
  - Original & compressed size (in bits)
  - **Compression Ratio**
  - **Entropy**
  - **Average codeword length**
  - **Coding Efficiency (%)**
- Highlights the **best-performing algorithm** in green
- Shows Huffman codeword table & probability distribution
- Customizable Golomb parameter **M**
- Random test sequence generator for Arithmetic Coding

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/tw1tch-dev/data-compression-algorithms
cd data-compression-algorithms

# Install dependencies (only Streamlit + standard library)
pip install streamlit

# Run the app
streamlit run app.py
```

The app uses **pure Python implementations** — no external compression libraries required!

## Supported Input Types

| Input Example                            | Available Algorithms                     |
|------------------------------------------|-------------------------------------------|
| `Hello world!!!!`                        | LZW, Huffman, RLE, Arithmetic            |
| `0000001111111100000011111`              | RLE (best), Huffman, Arithmetic         |
| `1,3,0,0,0,5,12,0,0,1500`                | Golomb (best), RLE                        |
| Any regular text                         | All except Golomb                         |

## Formulas Used

All mathematical expressions in the app are based on classic Information Theory:

| Measure                  | Formula                                                                                         | Description                                      |
|--------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------|
| **Entropy**      | $$H = -\sum_{i} p_i \log_2(p_i)$$                                                               | Theoretical lower bound (bits/symbol)            |
| **Average Codeword Length** | $$L_{\text{avg}} = \sum_{i} p_i \cdot l_i$$                                                    | Actual average bits used per symbol              |
| **Coding Efficiency**    | $$\eta = \frac{H}{L_{\text{avg}}} \times 100\%$$                                                | How close we are to the entropy limit            |
| **Compression Ratio**    | $$\text{Ratio} = \frac{\text{Original bits}}{\text{Compressed bits}}$$                         | Higher = better compression                      |

## Project Structure

```
├── app.py                  # Main Streamlit app
├── compression/
│   ├── __init__.py
│   ├── LZW.py
│   ├── Huffman.py
│   ├── RLE.py
│   ├── Golomb.py
│   ├── Arithmetic.py
│   └── Metrics.py          # Entropy, bit counting, etc.
├── css/styles.css          # Custom styling
├── Demo.ipynb              # Demo file
└── README.md               # This file
```

## Educational Value

Perfect for:
- Computer Science / Information Theory students
- Understanding practical differences between theoretical algorithms
- Visualizing why certain methods outperform others on specific data
- Preparing for exams or projects on data compression


## Author

This project was proudly developed as a **team effort**.
