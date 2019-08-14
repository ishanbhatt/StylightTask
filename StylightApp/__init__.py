import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields

from StylightApp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

api = Api(app=app, version="1.0.0", title="Stylight - PAM Challenge",
          description="Stylight - PAM Challenge API Specification <style>.models {display: none !important}</style>")
# Nasty hack otherwise model would not disappear from the screen

name_space = api.namespace('', description='Stylight')

from StylightApp import routes
from StylightApp import models


db.create_all()