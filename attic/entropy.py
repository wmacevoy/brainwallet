#!/usr/bin/env python

import math

def fact(n):
    fact = 1
    for i in range(1,n+1): 
        fact = fact * i
    return fact

def comb(n,k):
    return fact(n)//(fact(n-k)*fact(k))

def perm(n,k):
    return fact(n)//(fact(n-k))

def log2_comb(n,k):
    return math.log(comb(n,k),2)

def log2_perm(n,k):
    return math.log(perm(n,k),2)

words = 10000
choose = 12
comb_entropy = log2_comb(words,choose)
perm_entropy = log2_perm(words,choose)

print "words=" + str(words) + " choose=" + str(choose) + " comb entropy=" + str(comb_entropy)+ " perm entropy=" + str(perm_entropy)

