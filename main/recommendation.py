import pickle

import redis
from .note import read_ratings

_o = None


class Recommendation:
    def __init__(self):
        self.redis_server = redis.Redis(host='localhost', port=6379, db=0,
                                        password='password_of_redis_password_of_redis')
        self.similarity_sorted = {}
        self.similarity = {}
        self.cost_seconds = 0.0
        self.update()

    def update(self):
        self.similarity = pickle.loads(self.redis_server.get('books_recommend:unsorted_similarity'))
        self.similarity_sorted = pickle.loads(self.redis_server.get('books_recommend:sorted_similarity'))
        c = self.redis_server.get('books_recommend:cost_time')
        if c is None:
            self.cost_seconds = 0.0
        else:
            self.cost_seconds = pickle.loads(c).total_seconds()


    def regenerate(self):
        read_ratings.main_flow()
        self.update()
        pass


if _o is None:
    _o = Recommendation()


def get_similarity():
    return _o.similarity


def get_similarity_sorted():
    return _o.similarity_sorted


def get_cost_seconds():
    return _o.cost_seconds


def update_similarity():
    _o.update()


def regenerate_similarity():
    _o.regenerate()


def get_redis_server():
    return _o.redis_server
