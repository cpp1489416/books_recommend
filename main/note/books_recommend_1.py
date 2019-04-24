#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pymysql
import pandas as pd
import sys
import numpy as np


# In[3]:


conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='password',db='books_recommend',use_unicode=True, charset="utf8")


# In[ ]:





# In[4]:


type(conn)


# In[5]:


users = pd.read_sql('select * from main_user', conn)


# In[6]:


ratings = pd.read_sql('select * from main_rating', conn)


# In[7]:


books = pd.read_sql('select * from main_book', conn)


# In[8]:


ratings.shape


# In[9]:


books.shape


# In[10]:


users.shape


# In[39]:


books['book_row'] = books.index


# In[40]:


books.tail()


# In[42]:


ratings = pd.merge(ratings, books, on='isbn')


# In[44]:


ratings.tail()


# In[45]:


ratings = ratings[['user_id', 'book_row', 'rating']]


# In[62]:


books.shape


# In[60]:


users.shape


# In[63]:


an = np.zeros((271379,278858))


# In[ ]:




