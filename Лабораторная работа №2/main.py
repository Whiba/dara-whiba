# -*- coding: utf-8 -*-

myfile = open("tolstoy.txt", "rb");
text = myfile.read();
text_memoty = text;

# cut text by tokens and find names and divide them by sex
for i in [',', '.', ':', ';', '!', '?', '-', '—', '(', ')', '«', '»']:
    text_memoty = text_memoty.replace(i, ' ')
mylist = text_memoty.split();

for word in mylist:
    myword = word.decode('utf-8')