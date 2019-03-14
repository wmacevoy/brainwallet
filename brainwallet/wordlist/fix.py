#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir) 

from phrases import Phrases

languages = [
    "chinese_simplified", 
    "chinese_traditional", 
    "english", 
    "french", 
    "italian", 
    "japanese", 
    "korean", 
    "spanish" ]

reserved = dict()

for el1 in range(len(languages)):
    language = languages[el1]
    phrases = Phrases.forLanguage(language)
    words = phrases.words[:]
    sequence = [None for i in range(len(words))]
    reuses = False
    for i in range(len(words)):
        word=words[i]
        if word in reserved:
            words[i]=None
            sequence[reserved[word]]=word
            reuses = True
    k=0
    changed = False
    for i in range(len(words)):
        word=words[i]
        if word == None: continue
        while sequence[k] != None: k = k + 1
        sequence[k] = word
        changed = changed or phrases.invWords[word] != k
        k = k + 1

    for k in range(len(words)):
        reserved[sequence[k]] = k

    if reuses:
        print ("%s reuses words in previous dictionaries." % language)
    if not changed:
        print ("%s is unchanged." % language)
    else:
        print ("%s is changed to:" % language)
        for word in sequence:
            print (word.encode('utf-8'))
        print ("end of %s changes." % language)
        print ("")
