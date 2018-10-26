# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:00:47 2018

@author: Niklas
"""
import pandas as pd
import nltk 
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
class tagFinder:    
    def __init__(self):
        df = pd.read_csv('data_wrangle/df_final.csv')
        df = df.dropna(subset=['reviewText'])['reviewText']
        self.df = df
        
    def generate(self,neighbors):
        revs = self.df.iloc[neighbors]
        tok = revs.apply(lambda x:nltk.word_tokenize(x))
        result = tok.apply(lambda x: nltk.pos_tag(x))
        adjs = []
        for i,row in result.iteritems():
            for item in row:
                if item[1]=='JJ':
                    adjs.append(item[0].lower())
                    tags = pd.DataFrame(adjs)
        return tags[0].value_counts()[0:10]
    




