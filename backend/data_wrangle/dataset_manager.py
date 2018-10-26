import pandas as pd
import json

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
                artists.append(self.df.iloc[i]['artist'])
                titles.append(self.df.iloc[i]['title'])
                genres.append(self.df.iloc[i]['root-genre'])

                a = {'artist': self.df.iloc[i]['artist'], 'title': self.df.iloc[i]['title'], 'genre': self.df.iloc[i]['root-genre']}
                similar_songs.append(a)

        # similar_songs = pd.DataFrame({'artist': artists, 'title': titles, 'genre': genres})
        
        return similar_songs
