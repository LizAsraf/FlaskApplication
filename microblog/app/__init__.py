from flask import Flask
from config import Config
from pymongo import MongoClient
# from dotenv import dotenv_values
import os

app = Flask(__name__)
app.config.from_object(Config)
# db_values = dotenv_values(".env")
db_url = os.getenv('DATABASE_URL_APP', default='db:27017')
db_user = os.getenv('MONGODB_USER', default='root')
db_password = os.getenv('MONGODB_PASSWORD', default='example') 
client = MongoClient(host=db_url["DATABASE_URL_APP"], username=db_user["MONGODB_USER"], password=db_password["MONGODB_PASSWORD"])
db = client['flask_db']
Users = db['Users']
Posts = db['Posts']



from app import routes