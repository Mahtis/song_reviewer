# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 12:46:28 2018

"""

import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
<<<<<<< HEAD
from sklearn import model_selection, feature_selection
from sklearn.grid_search import GridSearchCV

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
print(x2.columns)

test_subject = [[1, 3, 1.5, 0.01, 160, 1.5, 360, 0.1, 2000, 2000, 0, 0, 0, 1, 0, 0, 0 , 0]]
Average_songs = [[15.64196263824093, 0.6826506867800174, 0.4484535703680573, 0.5321808437085632, 38.5357393618285, 0.5132998471541234, 122.87624119051739, 1.1225869303031197, 511.4659606656581, 253.45189149513433, 0, 0, 1, 0, 0, 0, 0, 0],
[15.998103855433962, 0.7010364003535495, 0.4502715703447983, 0.528632954730562, 438.7370305151992, 0.5080946553629749, 124.06884334149247, 1.1496389228023156, 551.274425727412, 271.5967467157763, 0, 0, 1, 0, 0, 0, 0, 0]]

print(rtc_model.predict(Average_songs))


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
# rtc_best = RandomForestClassifier(class_weight='balanced', bootstrap=True, criterion= 'gini', max_depth= 20, 
# max_features= 5, min_samples_split=4, n_estimators= 200)

# rtc_best_model = rtc_best.fit(X_train,y_train)
# print(rtc_best_model.score(X_test,y_test))
# result3=pd.DataFrame(rtc_best_model.predict(X_test))
# result3.plot.hist()
# print(result3[0].value_counts(),result3[0].value_counts(normalize=True))

########




=======
# from sklearn import model_selection, feature_selection
# from sklearn.grid_search import GridSearchCV
# import pickle
from sklearn.externals import joblib

# plt.style.use('seaborn-deep')
class ReviewModel:
    def __init__(self):
        self.filename = 'song_review_rtc_model.joblib'
        self.model = self.get_model(self.filename)

    def fit_model(self):
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

        model = rtc_best.fit(X_train,y_train)
        print(model.score(X_test,y_test))
        # result3=pd.DataFrame(rtc_best_model.predict(X_test))
        # result3.plot.hist()
        # print(result3[0].value_counts(),result3[0].value_counts(normalize=True))

        joblib.dump(model, self.filename) 
        # pickle.dump(rtc_best_model, open(filename, 'wb'))
        return model

    ########

    def get_model(self, filename):
        try:
            model = joblib.load(filename)
        except FileNotFoundError:
            model = self.fit_model()
        # model = pickle.load(filename, 'rb')
        return model

    def predict(self, row):
        return self.model.predict([row])
>>>>>>> 270b91baca3bb9157983663110a3158c8b06bcf3

# plt.show()
        
