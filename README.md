# Basic setup guide

## Install mongodb
### Follow these steps for installing mongo on your ubuntu enviroment
### https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/


## importing dataset
### install ml-latest.zip from https://grouplens.org/datasets/movielens/latest/
### unzip and move to project directory
### run import_to_mongo.py


## Set up your venv
### Run these commands in your project directory
### python3 -m venv venv
### source venv/bin/activate
### pip install -r requirements.txt


## create the index
### mongosh
### use movielens_db
### db.movies.createIndex({ title: "text" })

## running server
### navigate to ADatabase directory 
### python3 manage.py runserver 0.0.0.0:8000
