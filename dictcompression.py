# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:22:00 2019

@author: Lizerhigh
"""
class Block:
    def __init__(self, letter='', offset=0, length=0):
        self.let = letter
        self.offset = offset
        self.len = length
        
    def __getitem__(self, key):
        return '0' if bool(self.let) else '1'
    
    def __call__(self):
        if self.let:
            return self.let
        else:
            #print(f"[{self.offset-1}|{self.len-1}]")
            s = (self.offset-1)*16 + (self.len-1)
            return bytes([s//256, s%256])
        
    def __repr__(self):
        return f"{self.let}" if self.let else f"[{self.offset}|{self.len}]"
    
    def __str__(self):
        return self.__repr__()

def count(blocks):
    return bytes([int(''.join([x[0] for x in blocks]), 2)])
    
def compress(mes):
    r_buf_l = 15
    s_buf_l = 4095
    i = 0
    output = []
    ret = b''
    while i < len(mes):
        j = max(0, i - s_buf_l)
        flag = 0
        mi = i
        while j < i:
            if mes[i] == mes[j]:
                st = j
                sti = i
                while (j+1 < len(mes))and(i+1 < len(mes))and(mes[i+1] == mes[j+1])and(j-st < r_buf_l):
                    i += 1
                    j += 1
                if flag:
                    if j-st+1>output[-1].len:
                        output[-1] = Block(offset=i-j, length=j-st+1)        
                        mi = i
                else:
                    output.append(Block(offset=i-j, length=j-st+1))
                    mi = i
                    flag = 1
                i, j = sti, st 
            j += 1
        i = mi
        if (output)and(output[-1].len == 1):
            output[-1] = Block(letter=bytes([mes[i]]))
        if (i == j)and(not flag):
            output.append(Block(letter=bytes([mes[i]])))
        i += 1
        if len(output)==8:
            ret += count(output) + b''.join([x() for x in output])
            output = []
    if output:
        c = -len(output)%8
        output += [Block(letter=b'0') for x in range(c)]
        ret += count(output) + b''.join([x() for x in output]) + bytes([c])
    else:
        ret += bytes([0])
    return ret

def decompress(mes):
    i = 0
    ret = b''
    while i < len(mes):
        if i == len(mes)-1:
            ret = ret[:-mes[i]]
            break
        a = bin(mes[i])[2:]
        a = '0'*(-len(a)%8)+a
        for j in range(8):
            i += 1
            if a[j] == '0':
                ret += mes[i:i+1]
            else:
                i += 1
                length = mes[i-1]*256 + mes[i]
                length, offset = length%16+1, length//16+1
                #print(ret, offset, length)
                while length>0:
                    ret += bytes([ret[-offset]])
                    length -= 1
        i += 1
    return ret

import time

f = open(input('Input path to file to compress> '), 'rb')
lines = b''.join(f.readlines())
f.close()
f = open(input('Input out file path> '), 'wb')
print(time.ctime())
f.writelines([compress(lines)])
f.close()
print(time.ctime())

f = open(input('Input path to file to decompress> '), 'rb')
lines = b''.join(f.readlines())
f.close()
f = open(input('Input out file path> '), 'wb')
f.writelines([decompress(lines)])
f.close()
    
#a = b'aaabbbaabababbabjkvliwygf627u3djjskbcyuif76c87y8efghjkdfghjk'
#b = compress(a)
#print(b, f'len = {len(b)} Bytes')
#c = decompress(b)
#print(c, f'len = {len(c)} Bytes')