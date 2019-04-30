#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# Programmiertechniken in der Computerlinguistik II
# Übung 4 - Aufgabe 02
# Author: Silvio Magaldi und Vivien Angliker
# Date: 30.04.2019
# Matrikel-Nr: Silvio: 14-921-936 Vivien: 14-721-948


def longest_substrings(x: str, y: str):
    x = x.lower()
    y = y.lower()
    n = len(x)
    m = len(y)
    d = [[0 for _ in range(m)] for _ in range(n)]        # make the table (m x n)
    for i in range(0, n):
        if x[i] == y[0]:
            d[i][0] = 1                                  # fill a 1 into the table if it's the same character
    for j in range(0, m):
        if x[0] == y[j]:
            d[0][j] = 1
    for i in range(1, n):
        for j in range(1, m):
            if x[i] == y[j]:
                d[i][j] = d[i-1][j-1] + 1                # add one to the diagonal if it's the same lettre
    for i in range(0, n):
        s = ''
        for j in range(0, m):
            s += str(d[i][j])
            s += " "
        print(s + '\n')
    maxim_and_index = get_max(n, m, d)             
    maxim = maxim_and_index[0]
    maxim_i = maxim_and_index[1]
    char = get_char(maxim, maxim_i, x)
    print(maxim)
    print(char)

def get_max(n, m, d):       
    maxim = 0
    maxim_i = -1
    for i in range(0, n):               
        for j in range(0, m):
            if d[i][j] > maxim:                          # get the longest substring
                maxim = d[i][j]
                maxim_i = i
    return[maxim, maxim_i]


def get_char(maxim, maxim_i, x):
    start = maxim_i + 1 - maxim
    end = start + maxim
    char = x[start:end]                                  # get the characters of the longest substring
    return char



longest_substrings('Meisterklasse', 'Kleistermasse')     # call the function




