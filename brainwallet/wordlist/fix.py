#!/usr/bin/env python

import sys

from phrases import Phrases

langs = [
    "chinese_simplified", 
    "chinese_traditional", 
    "english", 
    "french", 
    "italian", 
    "japanese", 
    "korean", 
    "spanish" ]

reserved = dict()

for el1 in range(languages):
    language = languages[el1]
    phrases = Phrases.forLanguage[language]
    words = phrases.words[:]
    remap = dict()
    sequence = [None for i range(len(words))]
    for i in range(len(words)):
        word=words[i]
        if word in reserved[word]:
            words[i]=None
            sequence[reserved[word]]=word
    k=0
    changed = False
    for i in range(len(words)):
        word=words[i]
        if word == None: continue
        while sequence[k] != None: k = k + 1
        sequence[k] = word
        changed = changed or phrases.invWord[word] != k
        k = k + 1

    for k in range(len(words)):
        reserved[sequence[k]] = k

    if not changed:
        print ("%s is unchanged" % language)
    else:
        print ("%s is changed" % language)
        for word in sequence:
            print (word)
        print()
