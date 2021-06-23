import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:postgres@localhost:5432/file_manager'
    
    #'postgresql://postgres:tomererezor1@localhost:5432/menta4_from_heroku'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tomererezor1@localhost:5432/menta'       #menta db   
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    #SQLALCHAMY_ECHO = True

    #FROM https://stackoverflow.com/questions/53678781/how-to-configure-flask-uploads-properly-to-upload-files

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dcox'])
    UPLOADED_FILES_URL =   ' http://localhost:8000/'

    UPLOAD_FOLDER = os.path.join(basedir, 'flask_saved_files')
    
    UPLOADED_FILES_DEST =  os.path.join(basedir, 'flask_saved_files')
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'flask_saved_files')

    FLASK_SAVED_FILES_FOLDER = os.path.join(basedir, 'flask_saved_files')
    VUE_SAVE_FILES_FOLDER = os.path.join(basedir, '/client/public/vue_saved_files')
    SHARED_FOLDER = os.path.join(basedir, '/client/public/vue_saved_files')
    
    #FROM https://pythonhosted.org/Flask-Scss/
    SCSS_STATIC_DIR = 'app/static'
    SCSS_ASSET_DIR = 'app/static/assets'
    SCSS_LOAD_PATHS = [ '/Library/Ruby/Gems/1.8/gems/compass-0.11.5/frameworks/compass/stylesheets/']


    # FROM https://herbzhao.medium.com/vue-js-flask-flask-sqlalchemy-part-2-vue-js-plugins-4b6d1f61d30e
    # FOR UPLOAD FILES FROM VUE
    
    ########## CHECK!!! ##########
    # UPLOAD_FOLDER=r'saved_files\\'
    ########## CHECK!!! ##########

    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dcox']) IS ALREADY DEFINED UP
    
    #ANTHONIES ADVISE 
    #SQLALCHEMY_ECHO = True 
    #FROM https://stackoverflow.com/questions/53678781/how-to-configure-flask-uploads-properly-to-upload-files
      

    
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    print("SQLALCHEMY_MIGRATE_REPO IS : ", SQLALCHEMY_MIGRATE_REPO)
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    
        
    
