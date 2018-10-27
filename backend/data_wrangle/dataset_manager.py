import pandas as pd
import json
from ast import literal_eval

class datasetManager:
    def __init__(self):
        self.df = pd.read_csv('data_wrangle/df_final.csv')
    
    def get_similar_songs(self, indices):
        artists = []
        titles = []
        genres = []
        
        similar_songs = []
        for i in indices:
            if self.df.iloc[i]['title'] not in titles:
                artist = self.df.iloc[i]['artist']
                wanted_mbid = self.df.iloc[i]['first_song_mbid']
                album_songs = literal_eval(self.df.iloc[i]['songs'])
                title = ''
                for song in album_songs:
                    if song['mbid'] == wanted_mbid:
                        title = song['title']
                        titles.append(title)
                        break
                genre = self.df.iloc[i]['root-genre']

                a = {'artist': artist, 'title': title, 'genre': genre}
                similar_songs.append(a)

        # similar_songs = pd.DataFrame({'artist': artists, 'title': titles, 'genre': genres})
        
        return similar_songs
