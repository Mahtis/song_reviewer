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

