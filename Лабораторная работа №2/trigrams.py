#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from random import uniform
from collections import defaultdict
import pymorphy2

r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')
morph = pymorphy2.MorphAnalyzer()

def gen_lines(corpus):
    data = open(corpus)
    for line in data:
        yield line.decode('utf-8').lower()
        for i in [',', '.', ':', ';', '!', '?', '-', '—', '(', ')', '«', '»']:
            line = line.replace(i, ' ')

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(corpus):
    mymodel = []
    mymodel_mem = []
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)
    far_count = 0
    fan_count = 0
    hys_count = 0


    namef = "model" + corpus
    myfile = open(namef + ".txt", "w")

    fan_f = open("fantasy.txt", "rb")
    text_fan = fan_f.read();
    mylist_fan = set(text_fan.split())
    hys_f = open("history.txt", "rb")
    text_hys = hys_f.read();
    mylist_hys = set(text_hys.split())
    far_f = open("fairytales.txt", "rb")
    text_far = far_f.read();
    mylist_far = set(text_far.split())

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1


    for (t0, t1, t2), freq in tri.iteritems():
            if (freq/bi[t0, t1]) < 0.4 and (freq/bi[t0, t1]) > 0.2 and t0 != "$" and t1 != "$":
                textString = t0 + u" " + t1 + u" " + t2 + u" " + str(freq / bi[t0, t1])
                mymodel.append(textString)

    for myitem in mymodel:
        mylist = myitem.split()[0:2]
        f_found = True
        for myitemlist in mylist:
            myword = myitemlist
            p = morph.parse(myword)[0]
            if set(p.tag.grammemes) & set(['CONJ', 'PNCT', 'NPRO', 'PRCL', 'PREP', 'Name', 'Patr' ]):
                f_found = False

        if f_found :
            mymodel_mem.append(myitem)
            myfile.write((u"%s\n" % myitem).encode('utf-8'))

    out = []
    for _ in mymodel_mem:
        for __ in _.split()[0:3]:
            out += [__]
    y = set(out)
    z = set([
        morph.parse(w)[0].normal_form for w in y
        if not set(morph.parse(w)[0].tag.grammemes) &
               set(['CONJ', 'PNCT', 'NPRO', 'PRCL', 'PREP', 'Name', 'Patr'])
    ])

    z_far = set([
        morph.parse(w.decode('utf-8'))[0].normal_form for w in mylist_far
    ])
    z_fan = set([
        morph.parse(w.decode('utf-8'))[0].normal_form for w in mylist_fan
    ])
    z_hys = set([
        morph.parse(w.decode('utf-8'))[0].normal_form for w in mylist_hys
    ])

    for_far = z & z_far
    for p in for_far:
        print p
        far_count += 1
    for_fan = z & z_fan
    for p in for_fan:
        print p
        fan_count += 1
    for_hys = z & z_hys
    for p in for_hys:
        print p
        hys_count += 1

    print 'far = ', far_count
    print 'fan = ', fan_count
    print 'hys = ', hys_count
    mymodel = []
    mymodel = mymodel_mem
    return mymodel_mem

if __name__ == '__main__':
    filename = 'test2.txt'
    model = train(filename)

