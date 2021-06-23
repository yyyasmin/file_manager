import os

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from io import BytesIO    

import pdb #DEBUGING
   
# FROM https://www.programmersought.com/article/15116850767/
from flask_cors import CORS  #Flask's cross-domain issues
# FROM https://www.programmersought.com/article/15116850767/

from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy


from config import basedir
import config

from app import current_app, db

from app.models import Ufile
from app.models import General_txt


from sqlalchemy import update

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
vue_bp = Blueprint(
    'vue_client_bp', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import file_select2

from app import *

import pdb  # DEBUGING


# sanity check route
@vue_bp.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')
  
	
@vue_bp.route('/add_file', methods=['GET', 'POST'])
def add_file():

    print(" ")
    print(" ")
    
    print("")
    print("IN : add_file  request.files.get('file') ",  request.files.get('file'))
    print("")
    print("")
    
    
    file_obj =  request.files.get('file')
    
    file_name = file_obj.filename
    file_data = file_obj.read()
    
    #pdb.set_trace()

    this_file_exist = Ufile.query.filter(Ufile.name == file_name).filter(Ufile.hide==False).first()
    if this_file_exist != None:
        flash("קובץ בשם זה כבר קיים במערכת ")
        return url_for('files.edit_files' )
        
    new_file = Ufile(file_name, file_data)  #find out how to set file_data
    db.session.add(new_file)           
    db.session.commit() 
    
    save_file_res = retirect(url_for(files.save_file_to_upload_folder(new_file)))
    print("")
    print("save_file_res: ", save_file_res)
           
    return "File saved successfully"

	
@vue_bp.route('/del_file', methods=['GET', 'POST'])
def del_file():

    print(" ")
    print(" ")
    
    print("")
        
    file_id =  request.get_json().get('id')
    print("IN : dlete_file  FILE-ID ",  file_id)
    print("")
    print("")
 
    to_be_deleted_file = Ufile.query.filter(Ufile.id == file_id).first()
    if to_be_deleted_file == None:
        flash("אין קובץ כזה ")
        return "No such file in system"
  
    to_be_deleted_file.hide = True
    db.session.commit()
           
    return jsonify({"status_msg": "File deleted successfully" })

   
# FROM https://www.programmersought.com/article/15116850767/
@vue_bp.route('/get_file_from_vue', methods=['GET', 'POST'])
def get_file_from_vue():
    file_obj = request.files['file']  # Get files in Flask
    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"
    #save document
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "1.jpg")     
    file_obj.save(file_path)
    return file_path
    print(" ")
    print(" ")
    
    print("")
    print("IN : add_file  request.files.get('file') ",  request.files.get('file'))
    print("")
    print("")
    
    
    file_obj =  request.files.get('file')
    
    file_name = file_obj.filename
    file_data = file_obj.read()
    
    #pdb.set_trace()

    this_file_exist = Ufile.query.filter(Ufile.name == file_name).filter(Ufile.hide==False).first()
    if this_file_exist != None:
        flash("קובץ בשם זה כבר קיים במערכת ")
        return url_for('files.edit_files' )
        
    new_file = Ufile(file_name, file_data)  #find out how to set file_data
    db.session.add(new_file)           
    db.session.commit() 
    
    save_file_res = retirect(url_for(files.save_file_to_upload_folder(new_file)))
    print("")
    print("save_file_res: ", save_file_res)
           
    return "File saved successfully"




@vue_bp.route('/files_by_upload', methods=['GET', 'POST'])
def files_by_upload():

    print("")
    print("")
    print(" IN files_by_upload")
        
    files = Ufile.query.filter(Ufile.hide==False).all()
    
    FILE_NAMES = []
    for f in files:
        print("FILE: ", f)
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f.name)
        print("SENDING FILE FULL PATH: ", full_path)
        FILE_NAMES.append({'name': f.name, 'id': f.id})
        
    print("jsonify FILES", jsonify(FILE_NAMES))
    
    #return send_file(BytesIO(f.data), attachment_filename=f.name, as_attachment=True) # SEND BINARY DATA
       
    return jsonify({
        'status': 'success',
        'FILES': FILE_NAMES
    })    
 

@vue_bp.route('/files_by_data', methods=['GET', 'POST'])
def files_by_data():
    print("")
    print("")
    print(" IN files_by_data")
        
    files = Ufile.query.filter(Ufile.hide==False).all()

    for f in files:
        print("SENDIN BY DATA FILE: ", f)
        return send_file(BytesIO(f.data), attachment_filename=f.name, as_attachment=True) # SEND BINARY DATA


  
@vue_bp.route('/prepare_for_jsonify', methods=['GET', 'POST'])
def prepare_for_jsonify(files):

    print("")
    print("")
    print("IN jsonify_fies")
    
    files_arr = []
    for f in files:
        f_data = f.data
        tmp_arr = {}   #JSON STYLE
        print("FILE: ", f.name)
        print("")
        tmp_arr['name'] = f.name
        tmp_arr['body'] = f.body
        tmp_arr['data'] = f_data
        files_arr.append(tmp_arr)
        
    #return jsonify({'FILES': files_arr})    
    return files_arr 
