# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:05:04 2019

@author: Lizerhigh
"""

from numpy import ceil

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

def compress(mes, encoding = 16):
    d = {'esc': 0}
    tree = {'esc': '0'}
    prev = []
    output = ''
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
            prev = crnt
    return output

def decompress(mes, encoding = 16):
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
    encoding = int(input('Enter message encoding len(4/8/16/32)> '))
    initmes = input('Enter a message to compress> ')
    print()
    commes = compress(initmes, encoding)
    print(f"\nCompressed message(bin): '{commes}'\nInitial message len(bytes) = {int(ceil(len(initmes)*encoding//8))}\nCompressed message len(bytes) = {int(ceil(len(commes)/8))}\n")
#    cm4 = add_z(commes, 4)
#    hexmes = ''.join(map(lambda y: hex(int(y, 2))[2:], [cm4[x*4:(x+1)*4] for x in range(len(cm4)//4)]))
#    print(f"Compressed message(hex): '{hexmes}'\n")
    decmes = decompress(commes, encoding)
    print(f"Decompressed message: '{decmes}'")