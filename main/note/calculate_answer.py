#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql
import math
import operator
import redis
import pickle


# In[2]:


def get_similarity():
    r = redis.Redis(host='localhost', port=6379, db=0, password='password_of_redis_password_of_redis')
    b = r.get('books_recommend:unsorted_similarity')
    print(type(b))
    s = pickle.loads(r.get('books_recommend:unsorted_similarity'))
    return s


# In[4]:


books_similarity = get_similarity()
type(books_similarity)


# In[ ]:




