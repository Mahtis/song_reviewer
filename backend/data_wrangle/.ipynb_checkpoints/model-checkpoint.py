import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
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

y = df['overall']
x = df[columns]

print(df.dtypes)
model = LinearRegression()
model.fit(x, y)
print(model.score(x, y))