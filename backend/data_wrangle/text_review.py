import markovify
import pandas as pd

class Reviewer:
    def __init__(self):
        df = pd.read_csv('data_wrangle/df_final.csv')
        df = df.dropna(subset=['reviewText'])
        self.df = df
    
    def generate(self, indices):
        t = ''
        for n in indices:
            t += self.df.iloc[n].reviewText

        text_model = markovify.Text(t, state_size=3)
        review = []
        for i in range(5):
            review.append(text_model.make_sentence())
        return review

