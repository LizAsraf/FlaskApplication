from flask import Flask
from config import Config
from pymongo import MongoClient
# from dotenv import dotenv_values
import os

app = Flask(__name__)
app.config.from_object(Config)
# db_values = dotenv_values(".env")
db_url = os.getenv('DATABASE_HOST_APP', default='db')
db_port = int(os.getenv('MONGODB_PORT', default='27017'))
db_user = os.getenv('MONGODB_USER', default='root')
db_password = os.getenv('MONGODB_PASSWORD', default='example') 
client = MongoClient( host=db_url , port=db_port , username=db_user , password=db_password )
db = client['flask_db']
Users = db['Users']
Posts = db['Posts']



from app import routes