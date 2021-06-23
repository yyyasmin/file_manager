from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db

from app.models import Resource, Document, Ufile
from app.models import General_txt

from app.forms import LoginForm, EditForm

from sqlalchemy import update

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
file = Blueprint(
    'files', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import file_select2

from app import *


@file.route('/', methods=['GET', 'POST'])
@file.route('/index', methods=['GET', 'POST'])
@file.route('/edit_files', methods=['GET', 'POST'])
def edit_files():

    print("")
    print("IN EDIT FILES")
    
    files = Ufile.query.filter(Ufile.hide==False).all()
    for f in files:
        print("In edit_files  FILE:  ", f.name, f.body )

    return render_template('edit_files.html', files=files)
    

#update selected file
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@file.route('/file_update/<int:selected_file_id>', methods=['GET', 'POST'])
def file_update(selected_file_id):
    
    ####import pdb; pdb.set_trace()
    
    file_select2(selected_file_id)	
    file = Ufile.query.get_or_404(selected_file_id)
	
    if request.method == 'GET':
        return render_template('update_file.html')
		
    #get data from form and insert to destinationgress db
    #######import pdb; pdb.set_trace() 	
    file.title = request.form.get('title')
    file.body = request.form.get('description')
    file.selected=False
    db.session.commit()  
    db.session.refresh(file)
	
    return redirect(url_for('files.edit_files'))		
#end update selected file 	

	
@file.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
        
    print("Request is: ", request)
    
    if request.method == 'GET':
        print("")
        print("")
        print("")
        print("CALLING ./upload_file.html")
        return render_template('./upload_file.html')
        
    print("Request is: ", request)
    if request.method == 'GET':
        return render_template('upload_file.html')
         
    #get data from form and insert to uploaded_filegress db
    body = request.form.get('description')

    file_obj = request.files.get('file_obj')
    
    #import pdb; pdb.set_trace()
    
    file_name = file_obj.filename
    file_data = file_obj.read()

    this_file_exist = Ufile.query.filter(Ufile.name == file_name).filter(Ufile.hide==False).first()
    if this_file_exist != None:
        flash("קובץ בשם זה כבר קיים במערכת ")
        return url_for('files.edit_files' )
        
    save_file_res = save_file_to_upload_folder(file_obj)
    print("")
    print("save_file_res: ", save_file_res)
        
    new_file = Ufile(file_name, file_data)  #find out how to set file_data
    db.session.add(new_file)           
    db.session.commit()  
    
    print("upload_file NEW UPLOADED FILR is: ", new_file.name)
    
    return redirect(url_for('files.edit_files'))		


@file.route('/save_file', methods=['GET', 'POST'])
def save_file_to_upload_folder(file_obj):

    print("")
    print("IN SSSSSSSAAAAAAAAAAAAAAAAVE_fsave_file_to_upload_folder= ", file_obj.filename)
    print("current_app.config['UPLOAD_FOLDER']= ", current_app.config['UPLOAD_FOLDER'])
    
    res = file_obj.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_obj.filename))
    flash('File successfully uploaded', res)
    return res

# FROM https://pythonise.com/series/learning-flask/sending-files-with-flask   - Text
# FROM https://www.youtube.com/watch?v=QjpbWAirMWw&t=3s    - Vedio
@file.route("/send_file/<path:filename>")
def send_file_from_upload_folder(filename):

    print("")
    print("IN SENNNNNNDDDDD send_file_from_upload_folder= ", file_obj.filename)
    print("safe_path: ", safe_path)
    safe_path = safe_join(current_app.config["UPLOAD_FOLDER"], filename)

    try:
        return send_from_directory(safe_path, as_attachment=True)
    except FileNotFoundError:
        abort(404) 
# FROM https://pythonise.com/series/learning-flask/sending-files-with-flask   - Text



    
@file.route('/replace_file', methods=['GET', 'POST'])
def replace_file():

    file = Ufile.query.filter(Ufile.selected==True).first()
    if file == None:
        flash("Please select a file to update ")
        return redirect(url_for('files.edit_files'))	

    db.session.commit()      
    db.session.refresh(file)

    return redirect(url_for('files.edit_files' ))   


@file.route('/replace_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def replace_file2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return replace_file() 	


	
@file.route('/delete_file', methods=['GET', 'POST'])
def delete_file():

    delete_file = Ufile.query.filter(Ufile.selected==True).first()
    if delete_file == None:
        flash("Please select a uploaded_file to delete first ")
        return url_for('files.edit_files' )
        
    delete_file.hide = True
    
    print("")
    print("")

    #import pdb; pdb.set_trace()
    print ("delete_file requesed to DELETE FILE is " + delete_file.name )

    #import pdb; pdb.set_trace()
    db.session.commit()  

    return redirect(url_for('files.edit_files')) 

@file.route('/delete_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def delete_file2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return delete_file() 	

##############document's uploaded_files###############

	
##############document's download_files###############	

from io import BytesIO
from flask.helpers import send_file
	
@file.route('/download_file', methods=['GET', 'POST'])
def download_file():

    print("HHHHHHHHHHHHere in download_file")
        
    ##import pdb; pdb.set_trace()
    
    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a file first ")
        return redirect(url_for('files.edit_files'))	

    ##import pdb; pdb.set_trace()
    
    downloaded_file = send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
    #print("Downloaded file: ", downloaded_file)
    #return render_template('edit_document_uploaded_files.html', document=document) 
 
    
    
@file.route('/download_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_file2(selected_file_id):
    downloded_file = file_select2(selected_file_id)
    ##import pdb; pdb.set_trace()
    return download_file()			

##############document's download_files###############	

	
		
