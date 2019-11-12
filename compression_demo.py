# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:05:04 2019

@author: Lizerhigh
"""
from numpy import ceil

def f_codes(d, base = 2):
    ret = {k: '' for k in d.keys()}
    d = [([k], v) for k, v in d.items()]
    if len(d) == 1:
        return {d[0][0][0]:'0'}
    while len(d) != 1:
        d = [(k, v) for k, v in sorted(d, key=lambda x: x[1])]
        d, mins = d[base:], d[:base]
        for x in range(len(mins)):
            for y in mins[x][0]:
                ret[y] = str(x)+ret[y]
        d.append((sum(map(lambda x: x[0], mins), []), sum(map(lambda x: x[1], mins))))
    return ret

def compress(mes):
    d = {}
    for x in mes:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    d1 = f_codes(d)
    mes = ''.join([d1[x] for x in mes])
    return (mes, d, d1)

def decompress(mes, d):
    d1 = f_codes(d)
    ret = ''
    while mes:
        for k, v in d1.items():
            if mes.startswith(v):
                mes = mes[len(v):]
                ret += k
    return ret

if __name__ == '__main__':
    initmes = input('Enter a message to compress> ')
    print()
    commes, d, d1 = compress(initmes)
    general = sum(d.values())
    print('Freq table:')
    for k, v in d.items():
        print(f"'{k}': '{v/general*100:0.2f}%'")
    print('\nReplace table:')
    for k, v in d1.items():
        print(f"'{k}': '{v}'")
    statslen = len(''.join(d1.keys()))*2+sum(map(lambda x: ceil(len(x)/8), d1.values()))
    print(f"\nCompressed message(bin): '{commes}'\nInitial message len(bytes) = {len(initmes)*2}\nCompressed message len + dict len(bytes) = {int(ceil(len(commes)/8))} + {int(statslen)}\n")
#    cm4 = ('0'*(-len(commes)%4)+commes)
#    hexmes = ''.join(map(lambda y: hex(int(y, 2))[2:], [cm4[x*4:(x+1)*4] for x in range(len(cm4)//4)]))
#    print(f"Compressed message(hex): '{hexmes}'\n")
#    cm8 = ('0'*(-len(commes)%8)+commes)
#    chrmes = ''.join(map(lambda y: chr(int(y, 2)), [cm8[x*8:(x+1)*8] for x in range(len(cm8)//8)]))
#    print(f"Compressed message(chr): '{chrmes}'\n")
    decmes = decompress(commes, d)
    print(f"Decompressed message: '{decmes}'")
          