import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
import seaborn as sns

plt.style.use('seaborn-deep')
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
df = pd.read_csv('df_final.csv')
# print(df)
df_test = shuffle(df).head(10000)

df = df.dropna(subset = ['overall']) 
df['overall'] = df['overall'].astype(int)

# Pie chart 'Percentage of each score out of all reviews'
fig1, ax1 = plt.subplots()
colors = ['lavender', 'lightsteelblue', 'lightslategray', 'lightblue', 'slateblue']
ax1.pie([len(df[df['overall']==1]),len(df[df['overall']==2]),len(df[df['overall']==3]),len(df[df['overall']==4]),len(df[df['overall']==5])]
, autopct='%1.1f%%', colors=colors, labels=['1','2','3','4','5'])
ax1.axis('equal')
ax1.set_xlabel('Percentage of each score out of all reviews')

# Histogram of overall score distribution between songs in minor vs major scales
fig2, (ax1, ax2) = plt.subplots(1,2)
minors = df[df['chords_scale']=='minor']
majors = df[df['chords_scale']=='major']
ax1.hist([minors['overall'], majors['overall']], alpha=0.6, label=['minor', 'major'])
ax1.legend(loc='upper left')
ax1.set_xlabel('Overall score (out of 5)')

# Stack bar graph of overall score distribution between songs in different keys
keys = df['chords_key'].drop_duplicates()
margin_bottom = np.zeros(len(df['overall'].drop_duplicates()))
scales_overalls = []
for num, key in enumerate(keys):
    scales_overalls.append(df[df['chords_key'] == key]['overall'])
ax2.hist(scales_overalls, stacked=True, alpha=0.6, label=keys, normed=True)
ax2.legend(loc='upper left')
ax2.set_xlabel('Overall score (out of 5)')

fig2.suptitle('Overall score distribution between songs in minor vs. major scales')


# A rough scatter plotting of each audio description vs overall score
columns2 = ['average_loudness', 'dissonance', 'pitch_salience'] 
columns3 = ['dynamic_complexity', 'tuning_frequency', 'chords_strength', 'chords_changes_rate']
columns4 = ['danceability', 'bpm', 'beats_count', 'length']

fig3, axes2 = plt.subplots(1,3)
for i,t in enumerate(columns2):
    sns.stripplot(y=t, x= "overall", data=df,ax=axes2[i] ,alpha=0.01, jitter=0.2 )
fig4, axes3 = plt.subplots(1,4)
for i,t in enumerate(columns3):
    sns.stripplot(y=t, x= "overall", data=df,ax=axes3[i] ,alpha=0.01, jitter=0.2 )
fig5, axes4 = plt.subplots(1,4)
for i,t in enumerate(columns4):
    sns.stripplot(y=t, x= "overall", data=df,ax=axes4[i] ,alpha=0.01, jitter=0.2 )

fig2.tight_layout(rect=[0, 0.03, 1, 0.95])
fig3.tight_layout(rect=[0, 0.03, 1, 0.95])
fig4.tight_layout(rect=[0, 0.03, 1, 0.95])
fig5.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()