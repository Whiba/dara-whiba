# -*- coding: utf-8 -*-

import nltk
import re
import pymorphy2
from nltk import Counter

morph = pymorphy2.MorphAnalyzer()

text = u'Вася и Катя пошли гулять в парк. Там они встретили своих друзей Костю, Дениса и Марину. ' \
        u'Ребята играли в футбол. Вася и Катя поздоровались с друзьями и пошли на речку.';
name_male = []
name_female = []

# cut text by tokens and find names and divide them by sex
for i in [',', '.', ':', ';', '!', '?']:
    text = text.replace(i, '')
mylist = text.split();

for word in mylist:
    # выбираем с наибольшим score - оценка вероятности что данный набор правильный
    # так как сортировка по убыванию score, мы берем самый вероятный
    p = morph.parse(word)[0];
    if ('Name' in p.tag) == True:
        print(word)
        print(p.tag)
        if ('masc' in p.tag) == True:
            name_male.append(p.normal_form)
        if ('femn' in p.tag) == True:
            name_female.append(p.normal_form)

# search most popular male and female names
cntr_m = Counter(name_male)
popular_man = cntr_m.most_common(1)[0]

cntr_f = Counter(name_female)
popular_wom = cntr_f.most_common(1)[0]

# make a headline and print result
print("-------------------------------------------------------------------------------")
headline = popular_man[0] + u" и " + popular_wom[0]
print(u"'" + headline + u"'")
print(text)
