import pandas as pd
from sklearn.utils import shuffle
import numpy as np
from sklearn import model_selection, feature_selection
from sklearn.externals import joblib
from sklearn.neighbors import NearestNeighbors

class NnModel:
    def __init__(self):
        self.filename = 'song_review_nn_model.joblib'
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

        # X_train, X_test, y_train, y_test = model_selection.train_test_split(x2,y2,test_size=0.2)

        #### nearest neighbors ####
        neigh = NearestNeighbors(1000, 0.4)
        model = neigh.fit(x2)
        
        ## export model ##
        joblib.dump(model, self.filename) 
        return model

    ########

    def get_model(self, filename):
        try:
            model = joblib.load(filename)
        except FileNotFoundError:
            model = self.fit_model()
        return model

    def kneighbors(self, k, row):
        return self.model.kneighbors([row], k, return_distance=False)

