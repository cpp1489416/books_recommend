
import pandas as pd
import numpy as np
import tensorflow as tf

#%% dsa
ratings_df = pd.read_csv('main/ml-latest-small/ratings.csv')
ratings_df.tail()
movies_df = pd.read_csv('main/ml-latest-small/movies.csv')
movies_df.tail()
movies_df['movieRow'] = movies_df.index
movies_df.tail()

movies_df = movies_df[['movieRow', 'movieId', 'title']]
movies_df.tail()

movies_df.to_csv('moviesProcessed.csv', index=False, header=True, encoding='utf-8')

ratings_df = pd.merge(ratings_df, movies_df, on='movieId')

ratings_df.head()


ratings_df = ratings_df[['userId', 'movieRow', 'rating']]

ratings_df.tail()

ratings_df.to_csv('ratingsProcessed.csv', index=False, header=True, encoding='utf-8')

ratings_df.head()

usersNo = ratings_df['userId'].max() + 1


moviesNo = movies_df['movieId'].max() + 1

rating = np.zeros((moviesNo, usersNo))


#%%
flag = 0
ratings_df_length = np.shape(ratings_df)[0]
for index, row in ratings_df.iterrows():
    pass
