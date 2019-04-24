#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymysql
import math
import numpy as np


# In[2]:


users = pd.read_csv('main/BX-CSV-Dump/BX-Users.csv', sep=';', quotechar="\"", escapechar="\\", encoding='latin_1')
books = pd.read_csv('main/BX-CSV-Dump/BX-Books.csv',  sep=';', quotechar="\"", escapechar="\\", encoding='latin_1')
book_ratings = pd.read_csv('main/BX-CSV-Dump/BX-Book-Ratings.csv', sep=';', quotechar='\"', escapechar='\\', encoding='latin_1')


# In[3]:


db = pymysql.connect('localhost', 'root', 'password', 'books_recommend',charset='utf8')
cursor = db.cursor()


# In[ ]:


count = 0
for i in range(0, books.shape[0]):
    book = books.loc[i]
    sql = 'insert into main_book(isbn, title, author, published_year, publisher, image_url) values(%s, %s, %s, %s, %s, %s)'
    count += 1
    try:
        cursor.execute(sql, (book['ISBN'] if not pd.isnull(book['ISBN']) else 'default',
                             book['Book-Title'] if not pd.isnull(book['Book-Title']) else 'default',
                             book['Book-Author'] if not pd.isnull(book['Book-Author']) else 'default',
                             str(book['Year-Of-Publication'] if not pd.isnull(book['Year-Of-Publication']) else '-1'),
                             book['Publisher'] if not pd.isnull(book['Publisher']) else 'default',
                             book['Image-URL-L'] if not pd.isnull(book['Image-URL-L']) else 'default'))
        db.commit()
        if count % 10000 == 0:
            print('sent' + str(count))
    except error:
        print(error)
        


# In[ ]:


cursor.close()
db.close()


# In[6]:


users.tail()


# In[7]:


books.shape


# In[59]:


sql = 'insert into main_book(isbn, title, author, published_year, publisher, image_url) values(%s, %s, %s, %s, %s, %s)'

cursor.execute(sql, ('d',
                     'd',
                     'd',
                     'nan',
                     'd',
                     str(np.nan_to_num(np.NAN, 0))))
db.commit()


# In[119]:


book = books.loc[128896]


# In[120]:


pd.isnull(book['Publisher'])


# In[96]:


books.shape


# In[ ]:




