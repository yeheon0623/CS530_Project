import pandas as pd
from pymongo import MongoClient

# Connect to local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Create or use an existing database
db = client["movielens_db"]

# Function to import a CSV file into a MongoDB collection
def import_csv(filename, collection):
    print(f"Importing {filename} into '{collection}' collection...")
    df = pd.read_csv(f"ml-latest/{filename}")  # Load CSV using pandas
    db[collection].delete_many({})             # Clear existing data
    db[collection].insert_many(df.to_dict(orient="records"))  # Insert new data
    print(f"Imported {len(df)} records into '{collection}'")

# Import all required datasets
import_csv("movies.csv", "movies")
# Import ratings.csv in chunks to avoid memory overflow
print("Importing ratings.csv in chunks...")
chunk_size = 50000
for chunk in pd.read_csv("ml-latest/ratings.csv", chunksize=chunk_size):
    db["ratings"].insert_many(chunk.to_dict(orient="records"))
    print(f"Inserted chunk of {len(chunk)} records")
print("Finished importing ratings.csv")

import_csv("tags.csv", "tags")
import_csv("links.csv", "links")
import_csv("genome-tags.csv", "genome_tags")
# Import genome-scores.csv in chunks to avoid memory crash
print("Importing genome-scores.csv in chunks...")
chunk_size = 50000
for chunk in pd.read_csv("ml-latest/genome-scores.csv", chunksize=chunk_size):
    db["genome_scores"].insert_many(chunk.to_dict(orient="records"))
    print(f"Inserted chunk of {len(chunk)} records")
print("Finished importing genome-scores.csv")


