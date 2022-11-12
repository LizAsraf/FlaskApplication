from flask import Flask
from config import Config
from pymongo import MongoClient
from dotenv import dotenv_values

app = Flask(__name__)
app.config.from_object(Config)
db_values = dotenv_values(".env")
client = MongoClient(host=db_values["DATABASE_URL_APP"], username=db_values["MONGODB_USER"], password=db_values["MONGODB_PASSWORD"])
db = client['flask_db']
Users = db['Users']
Posts = db['Posts']

from app import routes