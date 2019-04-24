#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pyspark import SparkContext
from pyspark import SparkConf
from operator import add
from pyspark import SparkContext,SQLContext
from pyspark.sql import SQLContext
from pyspark.mllib.recommendation import ALS


# In[5]:


conf = SparkConf().setAppName("book_recommendation-server")
sc = SparkContext(conf=conf)


# In[11]:


books_raw_RDD = sc.textFile('main/BX-CSV-Dump/BX-Books.csv')


# In[16]:


books_raw_RDD.take(3)


# In[17]:


books_raw_data_header = books_raw_RDD.take(1)


# In[28]:


books_RDD = books_raw_RDD.filter(lambda line: line != books_raw_data_header)                            .map(lambda line: line.split(';'))                            .map(lambda tokens: (abs(hash(tokens[0][1:-1])) % (10 ** 8), tokens[1][1:-1], tokens[2][1:-1], tokens[3][1:-1], tokens[4][1:-1], tokens[5][1:-1]))                            .cache()


# In[29]:


books_RDD.take(1)


# In[30]:


books_titles_RDD = books_RDD.map(lambda x : (int(x[0]), x[1], x[2], x[3], x[4], x[5])).cache()


# In[31]:


books_titles_RDD.take(1)


# In[32]:


ratings_raw_RDD = sc.textFile('main/BX-CSV-Dump/BX-Book-Ratings.csv')


# In[33]:


ratings_raw_data_header = ratings_raw_RDD.take(1)[0]


# In[34]:


ratings_raw_data_header


# In[35]:


ratings_RDD = ratings_raw_RDD.filter(lambda line : line != ratings_raw_data_header)                                 .map(lambda line : line.split(';'))                                .map(lambda tokens: (int(tokens[0][1:-1]), hash(tokens[1][1:-1]) % 10 ** 8, int(tokens[2][1:-1])))


# In[36]:


ratings_RDD.take(10)


# In[37]:


book_ID_with_ratings_RDD = ratings_RDD.map(lambda x: (x[1], x[2])).groupByKey()


# In[39]:


def get_counts_and_average(ID_and_ratings_tuple):
    n = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (n, float(sum(x for x in ID_and_ratings_tuple[1]))/ n)


# In[40]:


book_ID_with_avg_ratings_RDD = book_ID_with_ratings_RDD.map(get_counts_and_average)


# In[41]:


book_ID_with_avg_ratings_RDD.take(10)


# In[42]:


book_ratings_count_RDD = book_ID_with_avg_ratings_RDD.map(lambda x : (x[0], x[1][0]))


# In[43]:


book_ratings_count_RDD.take(2)


# In[44]:


ratings_RDD.take(2)


# In[45]:


rank = 16
seed = 5
iterations = 10
regularization_parameter = 0.1


# In[46]:


model = ALS.train(ratings_RDD, rank=rank, seed=seed, iterations=iterations, lambda_=regularization_parameter )


# In[47]:


user_unrated_books_RDD = ratings_RDD.filter(lambda x : x[0] != 276725).map(lambda x : (276725, x[1])).distinct()


# In[48]:


user_unrated_books_RDD.take(9)


# In[49]:


predicted_RDD = model.predictAll(user_unrated_books_RDD)


# In[50]:


len(predicted_RDD.take(2))


# In[51]:


predicted_rating_RDD = predicted_RDD.map(lambda x: (x.product, x.rating))


# In[52]:


predicted_rating_RDD.takeOrdered(5, key=lambda x: -x[1])


# In[53]:


sqlContext=SQLContext(sc)


# In[65]:


ratings_df=sqlContext.read.format("jdbc").option("url","jdbc:mysql://localhost:3306/books_recommend")  .option("dbtable","main_rating").option("user","root").option("password","password").load()


# In[66]:


ratings_df.show()


# In[67]:


ratings_raw_rdd = ratings_df.rdd


# In[81]:


ratings_rdd  = ratings_raw_rdd.map(lambda x: (x.user_id, hash(x.isbn) % 10 ** 8, x.rating))


# In[82]:


ratings_rdd.count()


# In[97]:


model = ALS.train(ratings_rdd, rank=rank, seed=seed, iterations=iterations, lambda_=regularization_parameter )


# In[96]:


model.recommendProducts(300,10)


# In[1]:


i = 1


# In[2]:


i


# In[ ]:





# In[3]:


hhh 

#gvvv. v



# In[1]:


i = 3


# In[2]:


i


# In[ ]:




