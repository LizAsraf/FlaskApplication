from flask import Flask
from config import Config
from pymongo import MongoClient
# from app.utils import setting_statsd, StatsdMiddleware
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')


app.config.from_object(Config)
db_url = os.getenv('DATABASE_HOST_APP', default='db')
db_port = int(os.getenv('MONGODB_PORT', default='27017'))
db_user = os.getenv('MONGODB_USER', default='root')
db_password = os.getenv('MONGODB_PASSWORD', default='example') 
client = MongoClient( host=db_url , port=db_port , username=db_user , password=db_password )
db = client['flask_db']
Users = db['Users']
Posts = db['Posts']


from app import routes