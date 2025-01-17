import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# repo = UserRepository(app.config['DATABASE_URL'])


@app.route('/')
def index():
    return 'Welcome to Flask!'
