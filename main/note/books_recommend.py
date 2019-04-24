#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import numpy as np


# In[ ]:


import tensorflow as tf


# In[8]:


ratings_df = pd.read_csv('ml-latest-small/ratings.csv')


# In[9]:


ratings_df.tail()


# In[10]:


movies_df = pd.read_csv('ml-latest-small/movies.csv')


# In[11]:


movies_df.tail()


# In[12]:


movies_df['movieRow'] = movies_df.index


# In[13]:


movies_df.tail()


# In[14]:


movies_df = movies_df[['movieRow', 'movieId', 'title']]


# In[15]:


movies_df.tail()


# In[16]:


movies_df.to_csv('moviesProcessed.csv', index = False, header = True, encoding='utf-8')


# In[17]:


ratings_df = pd.merge(ratings_df, movies_df, on='movieId')


# In[18]:


ratings_df.head()


# In[19]:


ratings_df = ratings_df[['userId', 'movieRow', 'rating']]


# In[20]:


ratings_df.tail()


# In[36]:


ratings_df.to_csv('ratingsProcessed.csv', index = False, header = True, encoding='utf-8')


# In[36]:


ratings_df.head()


# In[75]:


usersNo = ratings_df['userId'].max() + 1


# In[76]:


moviesNo = movies_df['movieId'].max() + 1


# In[77]:


rating = np.zeros((moviesNo, usersNo))


# In[78]:


flag = 0
ratings_df_length = np.shape(ratings_df)[0]
for index, row in ratings_df.iterrows():
    rating[int(row['movieRow']), int(row['userId'])] = row['rating']
    flag += 1


# In[79]:


record = rating > 0


# In[80]:


record


# In[81]:


record = np.array(record, dtype = int)


# In[82]:


def normalize_ratings(rating, record):
    m, n = rating.shape
    rating_mean = np.zeros((m, 1))
    rating_norm = np.zeros((m, n))
    for i in range(m):
        idx = record[i, :] != 0
        rating_mean[i] = np.mean(rating[i, idx])
        rating_norm[i, idx] -= rating_mean[i]
    return rating_norm, rating_mean


# In[117]:


rating_norm, rating_mean = normalize_ratings(rating, record)


# In[93]:


arr = np.array([[1,2],[3,4],[5,6]])


# In[118]:


rating_mean = np.nan_to_num(rating_mean)
rating_norm = np.nan_to_num(rating_norm)


# In[ ]:





# In[113]:


np.nan_to_num(rating_mean)


# In[99]:


np.mean([1, 2, 3])


# In[95]:


arr[0, [False, True]]


# In[119]:


rating_norm


# In[ ]:


rating_mean


# In[37]:


fdsa


# In[ ]:




