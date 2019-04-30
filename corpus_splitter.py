#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# Programmiertechniken in der Computerlinguistik II
# Übung 4 - Aufgabe 01.1
# Author: Silvio Magaldi und Vivien Angliker
# Date: 30.04.2019
# Matrikel-Nr: Silvio: 14-921-936 Vivien: 14-721-948

from typing import BinaryIO
import random
import lxml.etree as ET
import gzip
import os

def split_corpus(infile: BinaryIO, targetdir: str, n: int):
    '''Takes a binary stream as input, a target directory for the 
    outfiles and an integer n indicating the size of test and development
    sets.
    Extracts all sentences from each extract and writes it into an 
    auxiliary file, separated by newlinecharacters. It iterates three
    times over this file, generating a file each as follows:
        1) Algortihm R for test set, size n.
        2) Algortihm R for development set, size n, not picking the
           ones already in test set.
        3) All not yet picked sentences into training set..
    '''
    training = os.path.join(targetdir, 'abstracts.txt.training.gz')
    test = os.path.join(targetdir, 'abstracts.txt.test.gz')
    development = os.path.join(targetdir, 'abstracts.txt.development.gz')
    #auxiliary file containing clean sections per line
    sections = os.path.join(targetdir, 'abstracts.txt.sections.gz')

    with gzip.open(training, 'wb') as tra,\
         gzip.open(test, 'wb') as tes,\
         gzip.open(development, 'wb') as dev:
        
        sec = gzip.open(sections, 'wb')
        for _, abstract in ET.iterparse(infile, tag='document'):
            #gather sentences
            doc = b''
            for sub in abstract:
                #contains: <title>, <section>
                if sub.tag == 'section':
                    section = b''
                    for sents in sub:
                        '''ET.tostring() result: 
                        <sentence>actual_sentence</sentence>\n   '''
                        sentence = ET.tostring(sents)
                        #cleanup sentence
                        sentence = (sentence.rstrip()
                                            .rstrip(b'</sentence>')
                                            .lstrip(b'<sentence>'))
                        section = section+ b' ' + sentence
                    doc = doc + b' ' + section
            sec.write(doc + b'\n')
            abstract.clear()
        sec.close()
        
        #Algorithm R
        with gzip.open(sections, 'rb') as sec:
            
            #test set
            s_tes = []  #string list
            h_tes = []  #hash list
            for i, sect in enumerate(sec):
                if i < n:
                    s_tes.append(sect)
                    h_tes.append(hash(sect)) 
                else:
                    r = random.randint(0,i)
                    if r < n:
                        s_tes[r] = sect
                        h_tes[r] = hash(sect)
            for element in s_tes:
                tes.write(element)
        
            #clear string list
            s_tes = []
        
            #reset file pointer to start
            sec.seek(0,0)
            #development set
            s_dev = []  #string list
            h_dev = []  #hash list 
            for i, sect in enumerate(sec):
                if len(s_dev) < n:
                    #check that sentence is not in test data
                    if hash(sect) not in h_tes:
                        s_dev.append(sect)
                        h_dev.append(hash(sect))
                else:
                    r = random.randint(0,i)
                    if (r < n) and (hash(sect) not in h_tes):
                        s_dev[r] = sect
                        h_dev[r] = hash(sect)
            for element in s_dev:
                dev.write(element)
            #clear string list
            s_dev = []
            
            #reset file pointer to start
            sec.seek(0,0)
            #training set
            for i, sect in enumerate(sec):
                #check that sentence is in neither test nor development set
                hs = hash(sect)
                if (hs not in h_dev) and (hs not in h_tes):
                    tra.write(sect)

    
def main():
    #set your target directory in next line
    directory = r'C:\UZH\PCL2\pcl2_ex4-master\pcl2_ex4-master\Korpusdaten'
    #rename your source file in next line
    abstracts = os.path.join(directory, 'abstracts.xml.gz')
    #set size of test and development sets in next line
    n = 1000
    with gzip.open(abstracts, 'rb') as infile:
        split_corpus(infile, directory, n)
        
if __name__ == '__main__':
    main()