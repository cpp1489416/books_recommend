#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pymysql
import math
import operator
import redis
import pickle
from datetime import datetime


# In[14]:


def get_ratings():
    db = pymysql.connect('localhost', 'root', 'password', 'books_recommend',charset='utf8')
    cursor = db.cursor()
    cursor.execute('select user_id, book_id, rating from main_rating')
    results = cursor.fetchall()
    
    ratings = {}
    for row in results:
        user_id = row[0]
        book_id = row[1]
        rating = row[2]
        if (float(rating) <= 3):
            continue
        if user_id not in ratings:
            ratings[user_id] = []
        ratings[user_id].append(book_id)
    cursor.close()
    db.close()
    del results
    del db
    del cursor
    return ratings


# In[15]:


def calculate_similarity(ratings):
    book_rating_times = {}
    book_appear_times = {}
    for user_id, book_ids in ratings.items():
        for i in range(0, len(book_ids)):
            book_i_id = book_ids[i]
            book_rating_times.setdefault(book_i_id, 0)
            book_rating_times[book_i_id] += 1
            
            for j in range(i + 1, len(book_ids)):
                book_j_id = book_ids[j]
                book_appear_times.setdefault(book_i_id, {})
                book_appear_times[book_i_id].setdefault(book_j_id, 0)
                book_appear_times[book_i_id][book_j_id] += 1
                
                book_appear_times.setdefault(book_j_id, {})
                book_appear_times[book_j_id].setdefault(book_i_id, 0)
                book_appear_times[book_j_id][book_i_id] += 1
                pass
            pass
        pass
    pass

    book_similarity_score = {}
    for i, relate_item in book_appear_times.items():
        for j, time in relate_item.items():
            score = time / math.sqrt(book_rating_times[i] * book_rating_times[j])
            book_similarity_score.setdefault(i, {})
            book_similarity_score[i].setdefault(j, 0)
            book_similarity_score[i][j] = score
    
    book_similarity_score_sorted = {}
    for i in book_similarity_score:
        book_similarity_score_sorted[i] = sorted(book_similarity_score[i].items(), key=operator.itemgetter(1), reverse=True)
        
    del book_rating_times
    del book_appear_times
    return book_similarity_score, book_similarity_score_sorted


# In[16]:


def main_flow():
    start_time = datetime.now()
    ratings = get_ratings()
    books_similarity, books_similarity_sorted = calculate_similarity(ratings)
    
    print('now start to flush to redis')
    r = redis.Redis(host='localhost', port=6379, db=0, password='password_of_redis_password_of_redis')
    r.set('books_recommend:unsorted_similarity', pickle.dumps(books_similarity))
    r.set('books_recommend:sorted_similarity', pickle.dumps(books_similarity_sorted))
    
    end_time = datetime.now()
    r.set('books_recommend:cost_time', pickle.dumps(end_time - start_time))
    
    print('flush ended')
    print((end_time - start_time).total_seconds())


# In[18]:


if __name__ == '__main__':
    main_flow()


# In[ ]:





# In[ ]:




