#!/usr/bin/env python

import inspect,math,os,sys,unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,parentdir) 

from phrases import Phrases

languages = [
    "ab",
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
    changed = False

    # put already reserved words at their index
    for i in range(len(words)):
        word=words[i]
        if word == None: continue
        if word in reserved:
            words[i]=None
            if phrases.invWords[word] != reserved[word]:
                changed=True
            sequence[reserved[word]]=word
            reuses = True

    # put new words in their place if not already reserved:
    for i in range(len(words)):
        word=words[i]
        if word == None: continue
        if words[i] in reserved: continue
        if sequence[i] != None: continue
        words[i] = None
        sequence[i] = word

    # put remaining words in sequence
    k=0
    for i in range(len(words)):
        word=words[i]
        if word == None: continue
        while sequence[k] != None: k = k + 1
        sequence[k] = word
        k = k + 1

    assert len(sequence)==len(words)
    for k in range(len(sequence)):
        if not sequence[k] in reserved:
            reserved[sequence[k]] = k
        else:
            assert reserved[sequence[k]] == k

    changes = 0
    for k in range(len(sequence)):
        word=sequence[k]
        oldIndex=phrases.invWords[word]
        newIndex=k
        if oldIndex != newIndex:
            changes = changes + 1

    if reuses:
        print ("%s reuses words in previous dictionaries." % language)
    if not changed:
        print ("%s is unchanged." % language)
    else:
        print ("%s is changed (%d/%d)=%f:" % (language,changes,len(words),float(changes)/float(len(words))))
        changes=0
        for k in range(len(sequence)):
            word=sequence[k]
            oldIndex=phrases.invWords[word]
            newIndex=k
            if oldIndex != newIndex:
                changes = changes + 1
                print "Change #%d: %s moved from %d to %d" % (changes,word.encode('utf-8'),oldIndex,newIndex)
        print ("%s new sequence:" % language)
        for word in sequence:
            print (word.encode('utf-8'))
        print ("end of %s new sequence." % language)
        print ("")
