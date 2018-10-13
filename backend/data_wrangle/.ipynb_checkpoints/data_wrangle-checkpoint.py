import pandas as pd
import json
import os 
import ijson
import collections

# read original datasets (MusicBrainz metadata of albums and Amazon user reviews)    
metadata = []
with open("mard_metadata.json", 'r') as f: 
    for line in f: 
        metadata.append(json.loads(line))

reviews = []
with open("mard_reviews.json", 'r') as f: 
    for line in f: 
        reviews.append(json.loads(line))


df_metadata = pd.DataFrame.from_dict(metadata)
df_metadata = df_metadata.dropna(subset = ['songs']) 

df_reviews = pd.DataFrame.from_dict(reviews)
df_reviews = df_reviews.drop(['helpful', 'reviewTime', 'reviewerID', 'reviewerName', 'summary', 'unixReviewTime'], axis=1)

df_metadata = df_metadata.merge(df_reviews, on='amazon-id', how='left')

# match MusicBrainz-id (mbid) and Amazon-id with path leading to AcousticBrainz audio-descriptors (separate json files)
directory = "/Users/Masavain/Downloads/mard/acousticbrainz_descriptors"
audio_descs_amazon_id = []
audio_descs_mbid = []
audio_descs_full_path = []
for entry in os.scandir(directory):
    amazon_id = entry.path.replace(directory + '/', '')[0:10]
    mbid = entry.path.replace(directory + '/', '')[11:47]
    audio_descs_amazon_id.append(amazon_id)
    audio_descs_mbid.append(mbid)
    audio_descs_full_path.append(entry.path)

df_audio_desc_paths = pd.DataFrame({"amazon-id": audio_descs_amazon_id, "first_song_mbid": audio_descs_mbid, "ad_path": audio_descs_full_path})
df_joined_metadata = df_metadata.merge(df_audio_desc_paths, on='amazon-id', how='right')

#drop useless columns
df_joined_metadata = df_joined_metadata.drop(['first-release-year', 'brand', 'artist_url', 'categories','related','salesRank', 'release-group-mbid', 'release-mbid'], axis=1)

#drop a single broken json-file
df_joined_metadata = df_joined_metadata.drop(df_joined_metadata.index[82899], inplace=False)
df_joined_metadata = df_joined_metadata.reset_index(drop=True)

#fetch AcousticBrainz audio-descriptors of each reviewed album's first track
df_joined_metadata['index'] = range(len(df_joined_metadata))
rows = []
for i in range(len(df_joined_metadata)):
    json_file = pd.read_json(df_joined_metadata.iloc[i]['ad_path'])
    row = []
    row.append(i)
    row.append(json_file[json_file.columns[0]]['spectral_complexity']['mean'])
    row.append(json_file[json_file.columns[0]]['average_loudness'])
    row.append(json_file[json_file.columns[0]]['dissonance']['mean'])
    row.append(json_file[json_file.columns[0]]['pitch_salience']['mean'])
    row.append(json_file[json_file.columns[0]]['dynamic_complexity'])
    row.append(json_file[json_file.columns[1]]['chords_scale'])
    row.append(json_file[json_file.columns[1]]['chords_key'])
    row.append(json_file[json_file.columns[1]]['key_scale'])
    row.append(json_file[json_file.columns[1]]['key_key'])
    row.append(json_file[json_file.columns[1]]['tuning_frequency'])
    row.append(json_file[json_file.columns[1]]['chords_strength']['mean'])
    row.append(json_file[json_file.columns[1]]['chords_changes_rate'])
    row.append(json_file[json_file.columns[2]]['bpm'])
    row.append(json_file[json_file.columns[2]]['danceability'])
    row.append(json_file[json_file.columns[2]]['beats_count'])
    row.append(json_file[json_file.columns[3]]['audio_properties']['length'])
    if 'genre' not in json_file[json_file.columns[3]]['tags']:
        row.append(['Other'])
    else:
        row.append(json_file[json_file.columns[3]]['tags']['genre'])

    rows.append(row)
    print(i)

columns = ['index','spectral_complexity', 'average_loudness', 'dissonance', 'pitch_salience', 
'dynamic_complexity', 'chords_scale', 'chords_key', 'key_scale', 'key_key','tuning_frequency', 
'chords_strength', 'chords_changes_rate', 'bpm', 'danceability', 'beats_count', 'length', 
'genre']

df_audio_desc_values = pd.DataFrame(rows, columns=columns)

# check that the dataframes have equal amount of rows
# print(df_audio_desc_values.shape)
# print(df_joined_metadata.shape)

# merge datasets to a single .csv file that is later used for the regression model's training
# and analysis/visualization of the data
df_final = df_joined_metadata.merge(df_audio_desc_values, on='index')

# check that the final dataset is of correct shape
# print(df_final.shape)

#write the final csv file
df_final.to_csv('df_final.csv', encoding='utf-8')


