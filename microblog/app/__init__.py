from flask import Flask
from config import Config
from pymongo import MongoClient
from app.utils import setting_statsd, StatsdMiddleware
import os

app = Flask(__name__)
# Setting statsd host and port
setting_statsd()
# Add statsd middleware to track each request and send statsd UDP request
app.wsgi_app = StatsdMiddleware(app.wsgi_app, "flask-monitoring")


app.config.from_object(Config)
db_url = os.getenv('DATABASE_HOST_APP', default='db')
db_port = int(os.getenv('MONGODB_PORT', default='27017'))
db_user = os.getenv('MONGODB_USER', default='root')
db_password = os.getenv('MONGODB_PASSWORD', default='example') 
client = MongoClient( host=db_url , port=db_port , username=db_user , password=db_password )
db = client['flask_db']
Users = db['Users']
Posts = db['Posts']


app = Flask(__name__)



from app import routes