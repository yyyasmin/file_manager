#FROM microblog/app/__init__.py
import logging
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import Config

from wtforms import *

from flask_migrate import Migrate

from flask_cors import CORS, cross_origin   #FOR THIS APP To TRANSFER FILES OVER DIFFERENT SERVERS


db = SQLAlchemy()

migrate = Migrate(compare_type=True)
bootstrap = Bootstrap()


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/__init__.py	
def create_app(config_class=Config):
    app = Flask(__name__)
        
    app.config.from_object(config_class)
    print("")
    print("app.config['UPLOAD_FOLDER']", app.config['UPLOAD_FOLDER'] )
        
    db.init_app(app)    
    
    migrate.init_app(app, db)    
    bootstrap.init_app(app)
    
    CORS(app) # This will enable CORS for all routes    
    # FROM https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#what-are-we-building
    # CORS(app, resources={r'/*': {'origins': '*'}})
    
    ### FROM https://github.com/mozilla/nunjucks/issues/296 ####
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    
    from app.gts.gts import gt

    from app.select.select import slct
    
    from app.files.files import file
    from app.vue_client_bp.vue_client_bp import vue_bp
    
    app.register_blueprint(gt)

    app.register_blueprint(slct)

    
    app.register_blueprint(file)
    app.register_blueprint(vue_bp)

    return app

from app import models
from app.models import *
from app import *





