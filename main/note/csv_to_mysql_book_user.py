#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import pymysql
import numpy as np


# In[3]:


users = pd.read_csv('main/BX-CSV-Dump/BX-Users.csv', sep=';', quotechar="\"", escapechar="\\", encoding='latin_1')
books = pd.read_csv('main/BX-CSV-Dump/BX-Books.csv',  sep=';', quotechar="\"", escapechar="\\", encoding='latin_1')
book_ratings = pd.read_csv('main/BX-CSV-Dump/BX-Book-Ratings.csv', sep=';', quotechar='\"', escapechar='\\', encoding='latin_1')


# In[34]:


db = pymysql.connect('localhost', 'root', 'password', 'books_recommend',charset='utf8')
cursor = db.cursor()


# In[35]:


for i in range(0, users.shape[0]):
    user = users.loc[i]
    sql = 'insert into main_user(id, name, location, age) values(%s, %s, %s, %s)'
    try:
        cursor.execute(sql, (str(user['User-ID']), 
                             'user of ' + str(user['User-ID']),
                             user['Location'] if not pd.isnull(user['Location']) else 'default',
                             str(np.nan_to_num(user['Age'], -1))))
        db.commit()
    except Error:
        print(Error)
        


# In[20]:


cursor.close()
db.close()


# In[4]:


book_ratings.tail()


# In[26]:


user = users.loc[1]


# In[36]:


user


# In[31]:


str(user['Age'])


# In[ ]:




