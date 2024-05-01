
class RLE:
    def __init__(self,):
        pass
    
    @staticmethod
    def run_length_encoding(string):
        encoded_string = ""  # Initialize an empty string to store the encoded result
        count = 1  # Initialize a counter to keep track of character repetitions
        vectorsNum = 1
        maxNum = 0
        for i in range(1, len(string)):
            # Check if the current character is the same as the previous one
            if string[i] == string[i - 1]:
                count += 1  # Increment the repetition count if characters are the same
            else:
                # If the current character is different from the previous one,
                # add the previous character and its repetition count to the encoded string
                encoded_string += string[i - 1] + str(count)
                if count > maxNum:
                    maxNum = count
                count = 1  # Reset the repetition count for the new character
                vectorsNum += 1
        # Add the last character and its repetition count to the encoded string
        encoded_string += string[-1] + str(count)
        return encoded_string, vectorsNum, maxNum
