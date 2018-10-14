# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 12:46:28 2018

@author: Niklas
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection, feature_selection
plt.style.use('seaborn-deep')

#read data from csv
df = pd.read_csv('df_final.csv')

#drop reviews that have no score
df = df.dropna(subset = ['overall']) 
df['overall'] = df['overall'].astype(int)

#create dummy variables for chords_scale and chords_key
dummy = pd.get_dummies(df['chords_scale'])
df = pd.concat([df, dummy], axis=1)

dummy = pd.get_dummies(df['chords_key'])
df = pd.concat([df, dummy], axis=1)

columns = ['spectral_complexity', 'average_loudness', 'dissonance', 'pitch_salience', 
'dynamic_complexity','tuning_frequency', 
'chords_strength', 'chords_changes_rate', 'bpm', 'danceability', 'beats_count', 'length', 'A', 'A#', 'B','C','C#','D','D#','E','F','F#','G','G#','minor','major']

df = shuffle(df)
y = df['overall']
x = df[columns]

# muuttujien P-arvojen tarkastelua. näitä käyttämällä n 1% parannus scoreen logregillä ja rndtreellä

p_values = pd.DataFrame()
p_values['column']= columns
p_values['P']=feature_selection.f_regression(x, y)[1]
p_values['F']=feature_selection.f_regression(x, y)[0]

good_cols=[]
for i,row in p_values.iterrows():
    if row.P < 0.05:
        print(row.column,row.P)
        good_cols.append(row.column)

y2 = df['overall']
x2 = df[good_cols]

X_train, X_test, y_train, y_test = model_selection.train_test_split(x2,y2,test_size=0.2)

#weights = {1:20,2:10,3:10,4:5,5:1} voi kokeilla ite säätää painoja myös (nää arvot ei toiminu)
logR = LogisticRegression(class_weight='balanced',solver='saga',max_iter=100)
model = logR.fit(X_train,y_train)
print(model.score(X_test,y_test))
result=pd.DataFrame(model.predict(X_test))


rtc = RandomForestClassifier(class_weight='balanced')

rtc_model = rtc.fit(X_train,y_train)
print(rtc_model.score(X_test,y_test))
result2=pd.DataFrame(rtc_model.predict(X_test))
result2.plot.hist()
print(result2[0].value_counts(),result2[0].value_counts(normalize=True))
        
"""
print(df.dtypes)
model = LinearRegression()
model.fit(X_train,y_train)
print(model.score(X_test,y_test))
"""

"""
Täällä testailin tarkastella vaan kappaleiden arvostelujen keskiarvoja, mutta 
tää ei tuloksia parantanut (päinvastoin).

grouped = []
for path,group in df.groupby('ad_path'):
    score = group.overall.mean()
    review = group.iloc[0].drop('overall')
    review['overall']=round(score)
    grouped.append(review)

df_grouped = pd.DataFrame(grouped)
 

y2 = df_grouped['overall']
x2 = df_grouped[columns]
X_train2, X_test2, y_train2, y_test2 = model_selection.train_test_split(x,y,test_size=0.2)

model2 = LogisticRegression(class_weight='balanced',solver='sag',max_iter=1000)
model2 = model2.fit(X_train2,y_train2)
print(model2.score(X_test2,y_test2))



p_values2 = pd.DataFrame()
p_values2['column']= columns
p_values2['P']=feature_selection.f_regression(x2, y2)[1]
p_values2['F']=feature_selection.f_regression(x2, y2)[0]

good_cols2=[]
for i,row in p_values2.iterrows():
    if row.P < 0.05:
        print(row.column,row.P)
        good_cols.append(row.column)
        
"""
