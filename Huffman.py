from logging import root
import os
import heapq

#creating a node for the heap

class Node:
    def __init__(self,char,freq):
        self.char=char #the character at the node
        self.freq=freq  #the frequency of the character
        self.left=None  #left and right children of the character
        self.right=None
    def __lt__(self,other): # we need these comparators for using heapq functions
        return self.freq<other.freq
    def __eq__(self,other):
        if other==None:
            return False
        if(not isinstance(other,Node)):
            return False
            
        return self.freq==other.freq
    
    
#The class used for compression
class Compressor:
    def __init__(self):
        self.heap=[]    #the heap used in huffman coding
        self.codes={}   #the characters mapped to the codes
        self.reverse_codes={} #the codes mapped to the characters
        
        
    def make_frequency_dict(self,text):#returns a dict which stores the frequency of each letter.
        frequency={}
        for i in text:
            if i not in frequency:
                frequency[i]=0
            frequency[i]+=1
        return frequency
    
    def make_heap(self,frequency):#puts each letter in a heap according to their frequency
        for key in frequency:
            node=Node(key,frequency[key])
            heapq.heappush(self.heap,node)
            
        while len(self.heap)>1:
            node1=heapq.heappop(self.heap)
            node2=heapq.heappop(self.heap)
            node=Node(None,node1.freq+node2.freq)
            node.right=node2
            node.left=node1
            heapq.heappush(self.heap,node)

            
    def get_codes(self,node,now_string):#assigns codes to the charactes
        if (node==None):
            return
        if node.char!=None:
            self.codes[node.char]=now_string
            self.reverse_codes[now_string]=node.char
            return
        self.get_codes(node.left,now_string+"0")
        self.get_codes(node.right,now_string+"1")
        
        
        
    def make_codes(self):#wrapper function for get_codes
        root=heapq.heappop(self.heap)
        curr=""
        self.get_codes(root,curr)
        return root
    def get_encoded_text(self,text):#gives the coded text in string format
        encoded_text=""
        for character in text:
            encoded_text+=self.codes[character]
        return encoded_text
    
    
    def get_byte_array(self,padded_encoded_text):#returns a byte array given the padded encoded text
        b=bytearray()
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            b.append(int(byte,2))   #representation in base 2
        return b
    
    
    def pad_encoded_text(self,encoded_text):#adds padding to the text to make the length a multiple of 8 for binary.
        extra=8-len(encoded_text)%8
        for i in range(extra):
            encoded_text+="0"
        padded_info="{0:08b}".format(extra)
        encoded_text=padded_info+encoded_text
        return encoded_text
    
    
    def compress(self,path):#the main commpressor function
        filename, file_extension=os.path.splitext(path)
        output_path=filename+".bin"#using binary file for output
        output=open(output_path,'wb')
        input=open(path,'r')
        text=input.read()
        frequency=self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.make_codes()
        encoded_text=self.get_encoded_text(text)
        padded_encoded_text=self.pad_encoded_text(encoded_text)
        b=self.get_byte_array(padded_encoded_text)
        output.write(bytes(b))
        print("Compressed")
        return self.reverse_codes   #returns the reversed_code this can be used for getting the file back


#the class used for decompression
class Decompressor:
    def __init__(self,keys):
        self.keys=keys  #we only need the reverse mapping
    def remove_padding(self, padded_encoded_text):  #removing the padding 
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-extra_padding]
        return encoded_text
    
    def decode_text(self,encoded_text):#converting binary to string
        current_code=""
        decoded_text=""
        for bit in encoded_text:
            current_code+=bit
            if(current_code in self.keys):
                character=self.keys[current_code]
                decoded_text+=character
                current_code=""
        return decoded_text
        
    def decompress(self,path,ext):#Decompresses file at the given path with the key initialised
        filename,file_extension=os.path.splitext(path)
        out_path=filename+"_decompressed"+"."+ext
        file=open(path,'rb')
        out_file=open(out_path,'w')
        bit_string=""
        byte=file.read(1)
        while(len(byte)>0):
            byte=ord(byte)
            bits=bin(byte)[2:].rjust(8,'0')
            bit_string+=bits
            byte=file.read(1)
        encoded_text=self.remove_padding(bit_string)
        decoded_text=self.decode_text(encoded_text)
        out_file.write(decoded_text)
        print("Decompressed")
        return (out_path)
    
    
    
filepath=input()
C=Compressor()
key=C.compress(filepath)
D=Decompressor(key)
filename, file_extension=os.path.splitext(filepath)
D.decompress(filename+".bin",file_extension)