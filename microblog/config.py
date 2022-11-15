import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
# The SECRET_KEY configuration variable use by Flask and some of its extensions as the secret key as a cryptographic key, useful to generate signatures or tokens. 
# The Flask-WTF extension uses it to protect web forms against a nasty attack called Cross-Site Request Forgery or CSRF (pronounced "seasurf")
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    MONGODB_USER = os.environ.get('MONGODB_USER') or 'mongdbuser'
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD') or 'alab2006'
    DATABASE_URL = os.environ.get('DATABASE_URL') or "mongodb://localhost:27017/"