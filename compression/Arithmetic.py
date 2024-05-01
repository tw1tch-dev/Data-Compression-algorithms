
class Arithmetic:
    def __init__(self,):
        pass
    @staticmethod
    def initialize_encoder(symbols, probabilities):
        # Validate symbol and probability lengths
        assert len(symbols) == len(probabilities) > 0

        # Ensure that the sum of probabilities equals 1.0
        sum_probabilities = sum(probabilities)
        if sum_probabilities != 1.0:
            # Normalize probabilities to ensure they sum up to 1.0
            probabilities = [prob / sum_probabilities for prob in probabilities]

        # Convert symbols to lowercase for uniformity
        symbols = [symbol.lower() for symbol in symbols]

        # Cumulative probabilities for interval refinement
        cumulative_probabilities = [0]
        for prob in probabilities:
            cumulative_probabilities.append(cumulative_probabilities[-1] + prob)

        # Initial interval
        low = 0.0
        high = 1.0

        return low, high, cumulative_probabilities, symbols
    @staticmethod
    def encode_symbol(low, high, symbol, cumulative_probabilities, symbols):
        # Convert symbol to lowercase
        symbol = symbol.lower()

        # Check if symbol is valid
        assert symbol in symbols

        # Get symbol index and cumulative probability
        symbol_index = symbols.index(symbol)
        cumulative_prob = cumulative_probabilities[symbol_index]

        # Calculate new interval limits based on symbol probabilities
        interval_width = high - low
        new_low = low + interval_width * cumulative_prob
        new_high = low + interval_width * cumulative_probabilities[symbol_index + 1]

        return new_low, new_high
    @staticmethod
    def get_symbols():
        while True:
            symbols_input = input("Enter symbols separated by spaces: ")
            symbols = symbols_input.split()
            if all(symbol.isalpha() for symbol in symbols):
                return symbols
            else:
                print("Invalid input! Symbols must only contain alphabetic characters.")
    @staticmethod
    def get_probabilities():
        while True:
            probabilities_input = input("Enter probabilities separated by spaces: ")
            try:
                probabilities = [float(p) for p in probabilities_input.split()]
                if sum(probabilities) == 1.0:
                    return probabilities
                else:
                    print("Invalid input! Probabilities must sum up to 1.")
            except ValueError:
                print("Invalid input! Please enter numerical values for probabilities.")
    @staticmethod
    def encode_sequence(sequence, symbols, probabilities):
        low, high, cumulative_probabilities, symbols = Arithmetic.initialize_encoder(symbols, probabilities)
        encoded_value = 0.0

        for symbol in sequence:
            low, high = Arithmetic.encode_symbol(low, high, symbol, cumulative_probabilities, symbols)
            encoded_value = (low + high) / 2  # Update encoded value within the new interval

        return encoded_value

