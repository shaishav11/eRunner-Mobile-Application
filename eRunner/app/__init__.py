from flask import Flask
import os

DEBUG = True
app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.config.from_object(__name__)
#app.config['SECRET KEY'] = 'c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'

from app import views
