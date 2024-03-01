# config.py

# import os

# SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'

# import from other code

# import os
# # from dotenv import load_dotenv
# basedir = os.path.abspath(os.path.dirname(__name__))
# # load_dotenv(os.path.join(basedir, '.env'))

# class Config():
#     '''
#         Set config variables for the flask app
#         Using Environment variables where available.
#         Otherwise create the config variable if not done already
#     '''

#     FLASK_APP = os.getenv('FLASK_APP')
#     FLASK_DEBUG = os.getenv('FLASK_DEBUG')
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'Matthew is from Texas'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
#     SQLALCHEMY_TRACK_NOTIFICATIONS = False