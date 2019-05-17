#!/usr/bin/env python
# coding: utf-8

# In[67]:


import math


# In[68]:


train = {
    'a': { 'b', 'c', 'd', 'f' },
    'b': {'d', 'e', 'f'},
    'c': {'a'},
    'd': {'z'},
}


# In[69]:


main = dict()


# In[70]:


main


# In[71]:


def user_similarity(train):
    W = dict()
    for u in train.keys(): 
        for v in train.keys():
            if u == v:
                continue
            if u not in W:
                W[u] = {}
            W[u][v] = len(train[u] & train[v])
            W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
    return W


# In[72]:


W = user_similarity(train)


# In[73]:


W


# In[74]:


{'b', 'd', 'c'} & {'f', 'e', 'd'}


# In[75]:


def user_similarity_2(train):
    item_users = dict()


# In[76]:


W = user_similarity_2(train)


# In[77]:


train.items()


# In[78]:


print(W)


# In[79]:


train


# In[89]:


def user_similarity_2(train):
    item_users = dict()
    for u, items in train.items():
         for v in items:
                if v not in item_users:
                    item_users[v] = set()
                item_users[v].add(u)
                
    C = dict()
    N = {}
    for i, users in item_users.items():
        for u in users:
            if not u in N:
                N[u] = 0
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                if not u in C:
                    C[u] = dict()
                if not v in C[u]:
                    C[u][v] = 0
                C[u][v] += 1
            pass
    pass


# In[90]:


user_similarity_2(train)


# In[65]:


i = 3


# In[66]:


i


# In[96]:


import pandas as pd
import numpy as np
question_ids = 200000
mat = np.mat(np.zeros([question_ids,question_ids],dtype=int))


# In[98]:


mat.shape


# In[ ]:




