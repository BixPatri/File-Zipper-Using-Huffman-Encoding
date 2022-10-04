# File Compressor
## How To Run
1. Go to terminal and type python3 Huffman.py
2. Then give the complete name of the file you want to compress as input.


It will then compress and decompress the file simultaneously.
You can take diff with of the decompressed file with the original file.
## Basics
Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.
<br>
The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream. 

## References

https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/

https://www.youtube.com/watch?v=JCOph23TQTY&ab_channel=BhriguSrivastava
