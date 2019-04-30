#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# Programmiertechniken in der Computerlinguistik II
# Übung 4 - Aufgabe 01.1
# Author: Silvio Magaldi und Vivien Angliker
# Date: 30.04.2019
# Matrikel-Nr: Silvio: 14-921-936 Vivien: 14-721-948

from typing import BinaryIO
import json
import bz2

def mk_meme_corpus(infile_path: str,
            outfile_path: str, min_score: int, min_len: int, max_len: int):
    infile = bz2.open(infile_path, 'rt')
    outfile = bz2.open(outfile_path, 'wt', encoding='utf8')
    used_comments = set()                                     # make a set to avoid the doubles
    for line in infile:
        comment = json.loads(line)
        text = comment['body']                                # get the comment itself
        score = comment['score']                              # get the score
        length = len(text)                                    # get the length of the comment
        if min_score<score and min_len<length and max_len>length:
            comment_hash = hash(text)                         # store them in a hash
            if comment_hash not in used_comments:
                used_comments.add(comment_hash)
                outfile.write(text)                           # write the comment itself into the outfile


mk_meme_corpus('RC_2012-06.bz2', 'mk_meme_corpus.txt.gz', 100, 1, 50)