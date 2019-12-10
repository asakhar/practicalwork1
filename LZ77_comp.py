# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:22:00 2019

@author: Lizerhigh
"""
#from pickle import dumps, loads
from dataclasses import dataclass
import compression_adaptive_pro as huffman


@dataclass
class Block:
    offset : int
    length : int
    letter : int
    
    def __str__(self):
        return f'{self.offset}|{self.length}|{bytes([self.letter])}'
    
    def __repr__(self):
        return str(self)
    
    def __bool__(self):
        return True
    
    def __eq__(self, other):
        return self.offset == other.offset and self.length == other.length and self.letter == other.letter
    
    def to_bytes(self, s_buf, r_buf, sum_buf):
        block = az(az(bin(self.offset)[2:], s_buf) + az(bin(self.length)[2:], r_buf), sum_buf)
        return bytes(map(lambda x: int(x, 2), [block[i*8:(i+1)*8] for i in range(sum_buf//8)])) + bytes([self.letter])

    def from_bytes(data, s_buf, r_buf, sum_buf):
        data, letter = data[:-1], data[-1]
        link = az(''.join(map(lambda x: az(bin(x)[2:]), data)), sum_buf)
        return Block(int(link[:-r_buf], 2), int(link[-r_buf:], 2), letter)    

def l2(n):
    c = 0
    while n>0:
        n //= 2
        c += 1
    return c

def az(s, n=8):
    return '0'*(-len(s)%n) + s
    
def compress(mes, s_buf=4096, r_buf=16):
    s_buf -= 1
    r_buf -= 1
    i = 0
    output = []
    while i < len(mes):
        j = max(0, i - s_buf)
        mi = i
        block = None
        while (i+2 < len(mes))and(j < i):
            if mes[i] == mes[j]:
                stj = j
                sti = i
                while (i+2 < len(mes))and(j+2 < len(mes))and(mes[i+1] == mes[j+1])and(j-stj < r_buf):
                    i += 1
                    j += 1
                if not block or j-stj+1>block.length:
                    block = Block(i-j, j-stj+1, mes[i+1])
                    mi = i + 1
                i, j = sti, stj
            j += 1
        i = mi
        if not block:
            block = Block(0, 0, mes[i])
        output.append(block)
        i += 1
    return output

def decompress(blocks, initmes = b''):
    initmes = [x for x in initmes]
    for i in blocks:
        for j in range(i.length):
            initmes.append(initmes[-i.offset])
        initmes.append(i.letter)
    return bytes(initmes)

def dumps(blocks, s_buf, r_buf):
    output = b''
    s_buf, r_buf = l2(s_buf), l2(r_buf)
    sum_buf = s_buf + r_buf
    sum_buf += -sum_buf%8
    for i in blocks:
        output += i.to_bytes(s_buf, r_buf, sum_buf)
    return output

def loads(data, s_buf, r_buf):
    output = []
    s_buf, r_buf = l2(s_buf), l2(r_buf)    
    sum_buf = s_buf + r_buf
    sum_buf += -sum_buf%8
    n = sum_buf//8+1
    for i in range(len(data)//n):
        output.append(Block.from_bytes(data[i*n:(i+1)*n], s_buf, r_buf, sum_buf))
    return output

message = 'tdrfvghdudhviufiuvsdhlgchgvjbkktjyccjgvkkhvgoij;m;seivicuxhmslicjvxldfoifvvslormaaaaaaaaaaaaaaaaaaaaaaaaмама мыла рамуaaaaaauuvgkdbhslsviykdsrnjdfoulblicwlrehsmjiuercsmjrvilcsnfvuirofdsvjfkdhgfghdfkjfdsdfghjklsdfghjkl;dfghjkl;dfghjkldfghjkldfghjkldfghjkl;dfghjkl;dfghjkldfghjkl;'
#message = ''.join(chr(i+97) for i in range(500))*2
search_buffer =  31
replace_buffer = 7
encoding = 'utf-16'
file = 'compressed_message.lz77'
encoded_mes = message.encode(encoding)
compress_huffman = 1

com = compress(encoded_mes, search_buffer, replace_buffer)
print(*com, sep='\n')

f = open(file, 'wb')
dump = dumps(com, search_buffer, replace_buffer)
if compress_huffman:
    f.writelines([huffman.compress(dump)])
else:
    f.writelines([dump])
f.close()

f = open(file, 'rb')
if compress_huffman:
    load = b''.join(f.readlines())
    with_huffman_length = len(load)
    load = huffman.decompress(load)
else:
    load = b''.join(f.readlines())
dec = decompress(loads(load, search_buffer, replace_buffer))
decoded_mes = dec.decode(encoding)
f.close()


print('OK' if decoded_mes == message else 'Error')
print('Initial message length         =', len(encoded_mes))
print('Compressed message length      =', len(dump))
if compress_huffman:
    print('Compressed with huffman length =', with_huffman_length)


#com_bytes = to_bytes(com, search_buffer, replace_buffer)
#f = open(file, 'wb')
#f.writelines([com_bytes])
#f.close()

#dec_bytes = from_bytes(com_bytes, search_buffer, replace_buffer)
#print(*dec_bytes, sep='\n')
#dec = decompress(dec_bytes)
#print(dec)
