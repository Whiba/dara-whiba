# -*- coding: utf-8 -*- 

import nltk 
import re 
import sys 
import pymorphy2 
from nltk import Counter 

morph = pymorphy2.MorphAnalyzer() 

myfile = open("new1.txt", "rb"); 
text = myfile.read(); 
name_male = [] 
name_female = [] 
text_memoty = text; 

# cut text by tokens and find names and divide them by sex 
for i in [',', '.', ':', ';', '!', '?', '-', '—', '(', ')', '«', '»']: 
    text_memoty = text_memoty.replace(i, ' ')
mylist = text_memoty.split(); 

for word in mylist: 
    # выбираем с наибольшим score - оценка вероятности что данный набор правильный
    # так как сортировка по убыванию score, мы берем самый вероятный
    myword = word.decode('utf-8')
    p = morph.parse(myword)[0];
    if ('Name' in p.tag) == True:
        # print(word)
        # print(p.tag)
        if ('masc' in p.tag) == True:
            name_male.append(p.normal_form)
        if ('femn' in p.tag) == True:
            name_female.append(p.normal_form)

# search most popular male and female names 
cntr_m = Counter(name_male) 
if cntr_m.__len__() != 0:
    popular_man = cntr_m.most_common(1)[0]
else: 
    popular_man = ''

cntr_f = Counter(name_female) 
if cntr_f.__len__() != 0: 
    popular_wom = cntr_f.most_common(1)[0]
else: 
    popular_wom = ''

# make a headline and print result 
print("-------------------------------------------------------------------------------") 
if type(popular_man) != str and type(popular_wom) != str: 
    headline = popular_man[0] + u" и " + popular_wom[0]
else: 
    if type(popular_man) == tuple and type(popular_wom) == str:
        headline = u"Меня зовут " + popular_man[0]
    if type(popular_wom) == tuple and type(popular_man) == str:
        headline = u"Меня зовут " + popular_wom[0]
print(u"'" + headline + u"'") 
print(text)