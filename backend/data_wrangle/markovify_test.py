import markovify
import pandas as pd
import re
import spacy

df = pd.read_csv('data_wrangle/df_final.csv')
df = df.dropna(subset=['reviewText'])


test_text = ''
for i in range(len(df['reviewText'])):
    test_text += df.iloc[i].reviewText


text_model = markovify.Text(test_text, state_size=3)

for i in range(5):
    print(text_model.make_sentence())
