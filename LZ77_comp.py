# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:22:00 2019

@author: Lizerhigh
"""
from pickle import dumps, loads
from dataclasses import dataclass



@dataclass
class Block:
    offset : int
    length : int
    letter : str
    
    def __str__(self):
        return f'{self.offset}|{self.length}|\'{self.letter}\''
    
    def __repr__(self):
        return str(self)
    
    def __bool__(self):
        return True
    
    def __eq__(self, other):
        return self.offset == other.offset and self.length == other.length and self.letter == other.letter
    
#    def to_bytes(self, sl, rl, encoding):
#        suml = sl+rl
#        suml += -suml%8
#        ret = az(az(bin(self.offset)[2:], sl)+az(bin(self.length)[2:], rl), suml) + az(bin(ord(self.letter))[2:], encoding)
#        return bytes([int(ret[i*8:(i+1)*8], 2) for i in range(len(ret)//8)])
#    
#    def from_bytes(bytes, sl, rl, encoding):
#        suml = sl + rl
#        suml += -suml%8
#        suml //= 8
#        link = az(''.join([az(bin(bytes[i])[2:], 8) for i in range(suml)]), suml*8)
#        letter = chr(int(''.join([az(bin(bytes[i])[2:], 8) for i in range(suml, len(bytes))]), 2))
#        offset, length = int(link[:-rl], 2), int(link[-rl:], 2)
#        return Block(offset, length, letter)        

def l2(n):
    c = 0
    while n>0:
        n //= 2
        c += 1
    return c

def az(s, n=16):
    return '0'*(-len(s)%n) + s
    
def compress(mes, s_buf=4096, r_buf=16):
    i = 0
    output = []
    while i < len(mes):
        j = max(0, i - s_buf)
        mi = i
        block = None
        while j < i:
            if mes[i] == mes[j]:
                stj = j
                sti = i
                while (mes[i+1] == mes[j+1])and(i+2 < len(mes))and(j+2 < len(mes))and(j-stj < r_buf):
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

def decompress(blocks):
    mes = ''
    for i in blocks:
        j = 0
        while j<i.length:
            mes += mes[-i.offset]
            j+=1
        mes += i.letter
    return mes

#def to_bytes(blocks, s_buf=4096, r_buf=16, encoding=16):
#    sl, rl = l2(s_buf), l2(r_buf)
#    ret = b''
#    for i in blocks:
#        ret += i.to_bytes(sl, rl, encoding)
#    return ret
#
#def from_bytes(mes, s_buf=4096, r_buf=16, encoding=16):
#    sl, rl = l2(s_buf), l2(r_buf)
#    suml = sl+rl+encoding
#    suml += -suml%8
#    suml //= 8
#    blocks = []
#    for i in range(len(mes)//suml):
#        blocks.append(Block.from_bytes(mes[i*suml:(i+1)*suml], sl, rl, encoding))
#    return blocks

message = 'aaaaaaaaaaaaaaaaaaaaaaaaмама мыла раму'
search_buffer =  4095
replace_buffer = 15
file = 'compressed_message.lz77'

com = compress(message, search_buffer, replace_buffer)
print(*com, sep='\n')

f = open(file, 'wb')
f.writelines([dumps(com)])
f.close()

f = open(file, 'rb')
dec = decompress(loads(b''.join(f.readlines())))
f.close()
print('OK' if dec == message else 'Error')


#com_bytes = to_bytes(com, search_buffer, replace_buffer)
#f = open(file, 'wb')
#f.writelines([com_bytes])
#f.close()

#dec_bytes = from_bytes(com_bytes, search_buffer, replace_buffer)
#print(*dec_bytes, sep='\n')
#dec = decompress(dec_bytes)
#print(dec)
