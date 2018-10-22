import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.utils import shuffle
import numpy as np
import seaborn as sns
import ast

plt.style.use('seaborn-deep')
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
df = pd.read_csv('data_wrangle/df_final.csv')
# print(df)
df_test = shuffle(df).head(10000)

df = df.dropna(subset = ['overall']) 
df['overall'] = df['overall'].astype(int)

#drop unused columns
df = df.drop(['artist','artist-mbid', 'confidence', 'imUrl', 'label',
'price','root-genre','songs','title','reviewText','first_song_mbid','ad_path','key_scale','key_key'], axis=1)

#convert strings of genres to lists
df['genre'] = df['genre'].apply(lambda x: ast.literal_eval(x))


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
    sns.stripplot(y=t, x= "overall", data=df,ax=axes2[i] ,alpha=0.01, jitter=0.1 )

fig4, axes3 = plt.subplots(2,2)
axli = axes3.flatten()
axli[0].set_ylim([0,20])
axli[2].set_ylim([0,0.75])
for i,t in enumerate(columns3):
    sns.stripplot(y=t, x= "overall", data=df,ax=axli[i] ,alpha=0.01, jitter=0.1 )

fig5, axes4 = plt.subplots(2,2)
axli = axes4.flatten()
axli[0].set_ylim([0, 2.25])
axli[2].set_ylim([0, 2500])
axli[3].set_ylim([0, 1500])
for i,t in enumerate(columns4):
    sns.stripplot(y=t, x= "overall", data=df,ax=axli[i] ,alpha=0.01, jitter=0.1 )

fig2.tight_layout(rect=[0, 0.03, 1, 0.95])
fig3.tight_layout(rect=[0, 0.03, 1, 0.95])
fig4.tight_layout(rect=[0, 0.03, 1, 0.95])
fig5.tight_layout(rect=[0, 0.03, 1, 0.95])

# fig1.savefig('fig1.png')
# fig2.savefig('fig2.png')
# fig3.savefig('fig3.png')
# fig4.savefig('fig4.png')
# fig5.savefig('fig5.png')


###
#find an average song of overall score 1 and 5 for display of average values:
###
# average song of overall score 1 (Bad song)
ones = df[df['overall']==1]
ones = ones.drop_duplicates(subset=['amazon-id'], keep=False)


genres = []
for i in range(len(ones)):
    for j in ones.iloc[i]['genre']:
        genres.append(j)
genres = pd.DataFrame.from_dict(genres)


bad_song = [999998,'amazon-id1',  1, ones['spectral_complexity'].mean(), ones['average_loudness'].mean(), ones['dissonance'].mean(),ones['pitch_salience'].mean(),
ones['dynamic_complexity'].mean(), ones['chords_scale'].mode()[0], ones['chords_key'].mode()[0], ones['tuning_frequency'].mean(),
ones['chords_strength'].mean(), ones['chords_changes_rate'].mean(), ones['bpm'].mean(), ones['danceability'].mean(), ones['beats_count'].mean(),
ones['length'].mean(), ['Other']]

# same for an average of overall score 5 (Good song)
fives = df[df['overall']==5]
fives = fives.drop_duplicates(subset=['amazon-id'], keep=False)

genres = []
for i in range(len(fives)):
    for j in fives.iloc[i]['genre']:
        genres.append(j)
genres = pd.DataFrame.from_dict(genres)

good_song = [ 999999,'amazon-id2', 5, fives['spectral_complexity'].mean(), fives['average_loudness'].mean(), fives['dissonance'].mean(),fives['pitch_salience'].mean(),
fives['dynamic_complexity'].mean(), fives['chords_scale'].mode()[0], fives['chords_key'].mode()[0], fives['tuning_frequency'].mean(),
fives['chords_strength'].mean(), fives['chords_changes_rate'].mean(), fives['bpm'].mean(), fives['danceability'].mean(), fives['beats_count'].mean(),
fives['length'].mean(), ['Other']]


print(bad_song)

print(good_song)

#plot some differences between the average one and five compared to overall ones and fives
df_ones_and_fives = pd.concat([ones,fives])

fig6, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

ax1.set_ylim([110, 140])
ax1.plot(1, good_song[13], 'bo', zorder=2)
ax1.plot(0, bad_song[13], 'ro', zorder=2)
sns.stripplot(y='bpm', x='overall', data=df_ones_and_fives,ax=ax1, alpha=0.1, zorder=1)


ax2.set_ylim([0.6, 2])
sns.stripplot(y='danceability', x='overall', data=df_ones_and_fives,ax=ax2, alpha=0.1, zorder=1)
ax2.plot(1, good_song[14], 'bo', zorder=2)
ax2.plot(0, bad_song[14], 'ro', zorder=2)

sns.stripplot(y='length', x='overall', data=df_ones_and_fives,ax=ax3, alpha=0.1, zorder=1)
ax3.set_ylim([0, 1000])
ax3.plot(1, good_song[16], 'bo', zorder=2)
ax3.plot(0, bad_song[16], 'ro', zorder=2)

sns.stripplot(y='dissonance', x='overall', data=df_ones_and_fives,ax=ax4, alpha=0.1, zorder=1)
ax4.plot(1, good_song[5], 'bo', zorder=2)
ax4.plot(0, bad_song[5], 'ro', zorder=2)
ax4.set_ylim([0.35, 0.50])


fig6.tight_layout(rect=[0, 0.03, 1, 0.95])
# fig6.savefig('fig6.png')
# plt.show()

