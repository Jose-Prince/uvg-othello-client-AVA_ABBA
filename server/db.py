from dotenv import load_dotenv 
import os 
from pymongo import MongoClient

load_dotenv() 

mongo_url = os.getenv("MONGO_CONNECTION")
client = MongoClient(mongo_url)
db = client.othello
