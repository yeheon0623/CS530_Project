import pymongo
from mongoengine import *
import mongoengine

import pymongo

#database connection functions
def connectDatabase():
    client = pymongo.MongoClient('mongodb://localhost:27017/')              #local address
    db = client['movielens_db']
    return db

class Links:
    movieId = StringField()
    tmdbId = StringField()
    imdbId = StringField()

    meta = {'collection': 'links'}

    def __init__(self):
        self.db = connectDatabase()
        self.links = self.db.links

class Tags:
    userId = StringField()
    movieId = StringField()
    tag = StringField()
    timestamp = StringField()

    meta = {'collection': 'tags'}

    def __init__(self):
        self.db = connectDatabase()
        self.tags = self.db.tags


class Movies:
    movieId = StringField()
    title = StringField()
    genres = StringField()

    meta = {'collection': 'movies'}



    def __init__(self):
        self.db = connectDatabase()
        self.movies = self.db.movies
        print(self.movies)


    def print(self):
        db = connectDatabase()
        genome_scores = db.genome_scores
        data1 = genome_scores.find()
        for data in data1:
            print(data.get('tagId'))

class Ratings:
    movieId = StringField()
    userId = StringField()
    rating = StringField()
    timestamp = StringField()

    meta = {'collection': 'ratings'}

    def __init__(self):
        self.db = connectDatabase()
        self.ratings = self.db.ratings


class GenomeTags:
    tagId = StringField()
    tag = StringField()
    meta = {'collection': 'genome_tags'}

    def __init__(self):
        self.db = connectDatabase()
        self.genome_tags = self.db.genome_tags


class GenomeScores:
    movieId = mongoengine.StringField()
    tagId = mongoengine.StringField()
    relevance = mongoengine.StringField()

    def __init__(self):
        self.db = connectDatabase()
        self.genome_scores = self.db.genome_scores