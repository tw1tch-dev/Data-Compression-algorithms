
class LZW:
    def __init__(self,):
        pass
    
    def LZW_encoder(self, file):
        """
        this function encodes the given file using LZW algorithm "lossless technique"
        input:
        file(String)----------> file to compress
        output:
        encoded_file(list)----> list of integers represent the compressed file
        """
        temp_dict     = {chr(i):i for i in range(128)}
        index         = 0
        s             = 1
        encoded_file  = []
        max_index     = 128 
        while index < len(file):
            pattern = file[index:index+s]
            if (pattern in temp_dict) and (s <= len(file)):
                s += 1
                continue
            else:
                char         = file[index: index+s-1]
                encoded_file.append(temp_dict[char]) 
                temp_dict.update({pattern: max_index})
                index        = index + s - 1 
                max_index   += 1
                s            = 1
        return encoded_file
    def LZW_decoder(self, encoded_file):
        """
        this function takes the encoded file then returns it back to the original file
        input:
        encoded_file(list)-------> list of integers represent the compressed file
        output:
        file(String)-------------> original file after decompressing the encoded_file
        """
        temp_dict     = {i:chr(i) for i in range(128)}
        before        = ""
        file          = ""
        max_index     = 128
        for index in encoded_file:
            if index in temp_dict:
                curr   = temp_dict[index]
            else :
                curr   = before[0] 
            pattern = before + curr[0]
            if pattern not in temp_dict.values():
                temp_dict.update({max_index:pattern})
                max_index += 1
            before = temp_dict[index]
            file += before
        return file

