from flask import Flask
app = Flask(__name__)
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import routes after initializing app, db, and jwt
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
