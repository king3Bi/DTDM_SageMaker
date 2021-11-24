import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

import re
from bs4 import BeautifulSoup

import pickle

import os
import glob

f = open("../../data_vi/vietnamese-stopwords.txt", "r")
stopwords = f.read()
stopwords = stopwords.replace('\n', ' ').split(' ')
stopwords = list(set(stopwords))

f = open("../../data_vi/teen_code.txt", "r")
teencodes = {}
for t in f.read().split('\n'):
    t = t.split('\t')
    teencodes[t[0]] = t[1]

def review_to_words(review):
    nltk.download("stopwords", quiet=True)
    stemmer = PorterStemmer()
    
    text = BeautifulSoup(review, "html.parser").get_text() # Remove HTML tags
    text = re.sub(r"[^a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]", " ", text.lower()) # Convert to lower case
    text = text.lower() # Convert to lower case
    text = text.strip()
    words = text.split(' ') # Split string into words
    words = [w for w in words if w not in stopwords] # Remove stopwords
    words = [w for w in words if w != '']
    new_words = []
    for w in words:
        if w in teencodes:
            new_words.append(teencodes[w])
        else:
            new_words.append(w)
    
    return new_words

def convert_and_pad(word_dict, sentence, pad=500):
    NOWORD = 0 # We will use 0 to represent the 'no word' category
    INFREQ = 1 # and we use 1 to represent the infrequent words, i.e., words not appearing in word_dict
    
    working_sentence = [NOWORD] * pad
    
    for word_index, word in enumerate(sentence[:pad]):
        if word in word_dict:
            working_sentence[word_index] = word_dict[word]
        else:
            working_sentence[word_index] = INFREQ
            
    return working_sentence, min(len(sentence), pad)