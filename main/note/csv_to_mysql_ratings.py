#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import pymysql
import numpy as np


# In[10]:


book_ratings = pd.read_csv('main/ml-latest-small/ratings.csv')


# In[11]:


book_ratings.tail()


# In[12]:


db = pymysql.connect('localhost', 'root', 'password', 'books_recommend',charset='utf8')
cursor = db.cursor()


# In[13]:


for i in range(0, book_ratings.shape[0]):
    rating = book_ratings.loc[i]
    sql = 'insert into main_rating( user_id, book_id, rating) values(%s, %s, %s)'
    try:
        cursor.execute(sql, (str(rating['userId']), 
                             str(rating['movieId']),
                             str(rating['rating'])))
        db.commit()
    except Error:
        print('some i ' + str(i))
        print(Error)
        


# In[5]:


cursor.close()
db.close()


# In[6]:


book_ratings.tail()


# In[25]:


rating = book_ratings.loc[1]


# In[26]:


rating['Book-Rating']


# In[27]:


str(rating['Book-Rating'])


# In[ ]:




