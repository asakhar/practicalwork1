# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:05:04 2019

@author: Lizerhigh
"""

from numpy import ceil
from infohw2 import draw_graph

def add_z(s, n):
    return '0'*(-len(s)%n)+s

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

def to_bytes(mes):
    n, mes = (-len(mes)%8), add_z(mes, 8)
    return bytes([n]) + bytes(map(lambda y: int(y, 2), [mes[x*8:(x+1)*8] for x in range(len(mes)//8)]))

def from_bytes(bmes):
    n, bmes = bmes[0], bmes[1:]
    ret = (''.join(map(lambda y: add_z(bin(y)[2:], 8), bmes)))[n:]
    return ret
    

def compress(mes, encoding = 16):
    d = {'esc': 0}
    tree = {'esc': '0'}
    prev = []
    output = ''
    steps = []
    for i in mes:
        if not i in d:
            d[i] = 1
            output += tree['esc'] + add_z(bin(ord(i))[2:], encoding)
        else:
            d[i] += 1
            output += tree[i]
        crnt = [k for k, v in sorted(list(d.items()), key=lambda x: x[1])]
        if prev != crnt:
            tree = f_codes(d)
            new_d = {(k if k!='esc' else '\\'): v for k, v in d.items()}
            steps.append(draw_graph(new_d, size=((1000*len(d))//17, (1400*len(d))//17))[0])
            prev = crnt
    #steps.append(draw_graph(d, size=(1000, 1400))[0])
    
    return to_bytes(output), steps, tree

def decompress(mes, encoding = 16):
    mes = from_bytes(mes)
    d = {'esc': 0}
    tree = {'esc': '0'}
    prev = []
    ret = ''
    while mes:
        if mes.startswith(tree['esc']):
            c, mes = mes[len(tree['esc']):len(tree['esc'])+encoding], mes[len(tree['esc'])+encoding:]
            c = chr(int(c, 2))
            ret += c
            d[c] = 1
        else:
            for i in tree:
                if mes.startswith(tree[i]):
                    ret += i
                    d[i] += 1
                    mes = mes[len(tree[i]):]
                    break
        crnt = [k for k, v in sorted(list(d.items()), key=lambda x: x[1])]
        if prev != crnt:
            tree = f_codes(d)
            prev = crnt
    return ret

if __name__ == '__main__':
    encoding = int(input('Enter message encoding len in bits(8/16/32)> '))
    initmes = input('Enter a message to compress> ')
    commes, steps, rescodes = compress(initmes, encoding)
    print('\nResultin codes:')
    for i in rescodes:
        print(f'{i}: {rescodes[i]}')
    
#    for i in range(len(steps)):
#        steps[i].save(f'sample2steps/step#{i+1}.png')
             
    print(f"\nCompressed message(bytes): {commes}\nInitial message len(bytes) = {int(ceil(len(initmes)*encoding//8))}\nCompressed message len(bytes) = {len(commes)}\n")
    decmes = decompress(commes, encoding)
    print(f"Decompressed message: '{decmes}'")