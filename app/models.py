
#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py3#from hashlib import md5
from flask import current_app
from app import db
#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/models.py

from datetime import datetime
from sqlalchemy.dialects.postgresql import INET
	
#FROM https://stackoverflow.com/questions/26470637/many-to-many-relationship-with-extra-fields-using-wtforms-sqlalchemy-and-flask
from sqlalchemy import event
#from common import UTCDateTime

#FROM https://botproxy.net/docs/how-to/how-to-handle-ordered-many-to-many-relationship-association-proxy-in-flask-admin-form/
from sqlalchemy.ext.associationproxy import association_proxy

  
############################################ Dst Form for cascade dropdown display     
### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
### FROM https://www.tutorialspoint.com/flask/flask_wtf.htm
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, DateField , FieldList, FormField, IntegerField
from wtforms import SelectField, validators, ValidationError

### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms.fields.html5 import DateField

from wtforms.fields import StringField
from wtforms.widgets import TextArea
 
# FROM https://stackoverflow.com/questions/60049631/flask-uploads-how-to-enforce-file-type-by-content-not-just-extension 
from flask_wtf.file import FileField, FileRequired

from datetime import datetime
from flask_login import UserMixin
   
### For Inheritance
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table


# FROM https://herbzhao.medium.com/vue-js-flask-flask-sqlalchemy-part-2-vue-js-plugins-4b6d1f61d30e
# FOR VUE FILES
from flask import Flask, render_template, jsonify, request, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS

# https://flask-marshmallow.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow

from werkzeug.utils import secure_filename
import os
# FROM https://herbzhao.medium.com/vue-js-flask-flask-sqlalchemy-part-2-vue-js-plugins-4b6d1f61d30e





#FROM https://hackersandslackers.com/forms-in-flask-wtforms/
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)


#from http://flask-appbuilder.readthedocs.io/en/latest/multipledbs.html for dealing with 2 data bases db
class Psps_db(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class Menta_db(db.Model):
	__bind_key__ = 'menta_db'
	id = db.Column(db.Integer, primary_key=True)

####################################### User
  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(50))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    is_super_user = db.Column(db.Boolean, nullable=True)
    school_logo_name = db.Column(db.String(200), nullable=True)  # FOR LAYOUT
    matya_logo_name =  db.Column(db.String(200), nullable=True)  # FOR LAYOUT
    
    def __init__(self , username ,password , email, is_super_user):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.is_super_user = is_super_user

    def get_is_super_user(self):
        return self.is_super_user == True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)	  # python 3
               
    def add(self,user):
        db.session.add(user)
        return session_commit ()

    def update(self):
        return session_commit()

    def delete(self,user):
        db.session.delete(user)
        return session_commit()

    def __repr__(self):
        return '<User %r>' % (self.username)
  
    ####################################### User


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.8/app/models.py

########################################## Parent_child_relationship

parent_child_relationship = db.Table('parent_child_relationship',
    db.Column('parent_id', db.Integer, db.ForeignKey('general_txt.id')),
    db.Column('child_id',  db.Integer, db.ForeignKey('general_txt.id'))
) 	
		   
########################################## Parent_child_relationship 
			   

############################################ General_txt 

class General_txt(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
 
    ufile_id =  db.Column(db.Integer, db.ForeignKey('ufile.id'), nullable=True)
        
    type = db.Column(db.String(50))     # for example" 'subject'
    
    h_name = db.Column(db.String(50))   # for example" 'חוזקה'
    e_name = db.Column(db.String(50))   # for example" 'Are of Subject'
    h_plural_name = db.Column(db.String(100))

    gt_type = db.Column(db.String(50))  # for example" 'Subject'
    class_name = db.Column(db.String(50))  # for example" 'Subject'

    title = db.Column(db.String(255), nullable=False)
    body =  db.Column(db.String(500))
    default = db.Column(db.Boolean)
    
    color_txt = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    table_color = db.Column(db.String(50), nullable=True)
    title_color = db.Column(db.String(50), nullable=True)
    odd_color = db.Column(db.String(50), nullable=True)
    even_color = db.Column(db.String(50), nullable=True)
    
    timestamp = datetime.utcnow()
    
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean) 


   # Anthonies suggestion
    children = db.relationship(
            'General_txt', secondary=parent_child_relationship,
            primaryjoin=(parent_child_relationship.c.parent_id == id),
            secondaryjoin=(parent_child_relationship.c.child_id == id),
            backref=db.backref('parent_child_relationship', lazy=False),
            lazy=False) 
                     
    __mapper_args__ = {
        'polymorphic_identity':'general_txt',
        'polymorphic_on':type
    }
    
    def get_parent(self, type):
        parents = [i for i in self.parent_child_relationship if i.type == type]
        #assert len(parents) <= 1
        if len(parents) > 0:
            return parents[0]
        return None
        #all_gts = General_txt.query.all()
        #for parent_gt in all_gts:
        #    if (parent_gt.is_parent_of(self) and parent_gt.type=='tag'):
        #        return parent_gt
        #return None
 
    def set_parent(self, general_txt):
        if not self.is_parent_of(general_txt):
            self.children.append(general_txt)

    def unset_parent(self, general_txt):
        if self.is_parent_of(general_txt):
            self.children.remove(general_txt)
    
    #Anthonies suggestion
    def is_parent_of(self, general_txt):
            return general_txt in self.children 
            
    def children_ids(self):
            return General_txt.query.join(
                parnet_child_relationship, (parnet_child_relationship.c.children_id == General_txt.id)).filter(
                    parnet_child_relationship.c.parent_id == self.id).order_by(
                        Generl_txt.title) 
                        
    def get_all_gts_of_type(self):
        return eval(self.gt_type).query.all()
                                
    def __init__(self ,title, body):
        self.title = title
        self.body = body
        
        self.timestamp = datetime.utcnow()        
        self.due_date = datetime.today()

        self.selected = False
        self.hide = False
        self.default = False
        
    def __repr__(self):
        return '<Dst %r>' % self.title
  
############################################ General_txt

class Gt_form(FlaskForm):
   
    gt_color_txt = StringField('שחור')
    gt_color = StringField('black')
    gt_title_color = StringField('gray')    
    gt_table_color = StringField('gray_table')
   
    gt_title = TextField("כותרת",[validators.Required("יש להכניס כותרת")])                                   
    gt_body =  TextField("תאור", render_kw={"rows": 70, "cols": 11})
    gt_type =  StringField('type')
    gt_class_name =  StringField('Class')
    gt_single_type_txt = StringField('single')
    gt_plural_type_txt = StringField('plural')
         
    submit = SubmitField("שמור")
    
    ### FROM https://stackoverflow.com/questions/44242802/python-flask-validate-selectfield
    def validate_tag(form):
        if not form.tag.data == None:
          raise ValidationError('יש לבחור נושא')


########################################## Resource
						   			   
class Resource(General_txt):

    __tablename__ = 'resource'
    __mapper_args__ = {'polymorphic_identity': 'resource'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body):
    
        self.h_name = 'מקורות'   
        self.e_name = 'Resource'  
            
        self.class_name = 'Resource'
        self.gt_type = 'Resource'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body)
   

class Document(General_txt):

    __tablename__ = 'document'
    __mapper_args__ = {'polymorphic_identity': 'document'}
       
    id = db.Column(db.ForeignKey(General_txt.id), primary_key=True)
    
    def __init__(self, title, body):
    
        self.h_name = 'מסמך'   
        self.e_name = 'Document'  
            
        self.class_name = 'Document'
        self.gt_type = 'Document'
        
        self.color_txt = 'black'
        self.color = '#00284d'
        self.editable = True     
        super(self.__class__, self).__init__(title, body)

############################################ Document  

  
########################################## U-File
                           						   
class Ufile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    data = db.Column(db.LargeBinary)   #file content
    
    name = db.Column(db.String(300),  nullable=True)
    body = db.Column(db.String(1000), nullable=True) 
    
    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)
    
    '''
    # FROM https://stackoverflow.com/questions/63690158/save-uploaded-image-to-database-on-flask
    rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser
    text = db.Column(db.Text)
    location = db.Column(db.String(300))
    pic_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
      return f'Pic Name: {self.name} Data: {self.data} text: {self.text} created on: {self.pic_date} location: {self.location}'
    # FROM https://stackoverflow.com/questions/63690158/save-uploaded-image-to-database-on-flask
    '''
    
    def __init__(self, name, data):

        self.name = name
        self.data = data
        self.hide = False
        self.selected = False


############################################ File  

	
##################################Student													
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(20), index=True)
    birth_date = db.Column(db.Date, nullable = True)
    grade  = db.Column('grade', db.String(10))
    background = db.Column('background', db.Text)

    timestamp = datetime.utcnow()
    registered_on = db.Column('registered_on' , db.Date) 

    selected = db.Column(db.Boolean)
    hide = db.Column(db.Boolean)

    def __init__(self, id, first_name, last_name ,birth_date, grade):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name	
        self.birth_date = birth_date
        self.grade = grade
        
        self.registered_on = datetime.utcnow()

        self.selected = False
        self.hide = False
        
        
    def add(self,student):
        db.session.add(student)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self,student):
        db.session.delete(student)
        return session_commit()
        
##################################Student

  
# from https://github.com/Leo-G/Freddy/blob/master/app/models.py		  
#Universal functions

def  session_commit ():
	try:
		db.session.commit()
	except SQLAlchemyError as e:
		db.session.rollback()
		reason=str(e)
		return reason
  