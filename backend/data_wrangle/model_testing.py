# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 12:46:28 2018

"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection, feature_selection
from sklearn.grid_search import GridSearchCV
import pickle
plt.style.use('seaborn-deep')

#read data from csv
df = pd.read_csv('data_wrangle/df_final.csv')

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


# param_grid = { "n_estimators"      : [10, 200],
#            "criterion"         : ["gini"],
#            "max_features"      : [3, 5],
#            "max_depth"         : [10, 20],
#            "min_samples_split" : [2, 4] ,
#            "bootstrap": [True, False]}
# grid_search = GridSearchCV(rtc, param_grid, n_jobs=-1, cv=2)
# grid_search.fit(X_train, y_train)
# print("grid search best params: ", grid_search.best_params_)
# grid search best params:  
# {}
# print("grid search best score ", grid_search.score(X_test, y_test))

#### rfc with best params ####
rtc_best = RandomForestClassifier(class_weight='balanced', bootstrap=True, criterion= 'gini', max_depth= 20, 
max_features= 5, min_samples_split=4, n_estimators= 200)

rtc_best_model = rtc_best.fit(X_train,y_train)
print(rtc_best_model.score(X_test,y_test))
result3=pd.DataFrame(rtc_best_model.predict(X_test))
result3.plot.hist()
print(result3[0].value_counts(),result3[0].value_counts(normalize=True))

filename = 'song_review_rtc_model.sav'
pickle.dump(rtc_best_model, open(filename, 'wb'))

########


plt.show()
        
