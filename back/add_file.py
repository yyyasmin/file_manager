
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
        FILE_NAMES.append(f.name)
        
    print("jsonify FILES", jsonify(FILE_NAMES))
    
    #return send_file(BytesIO(f.data), attachment_filename=f.name, as_attachment=True) # SEND BINARY DATA
       
    return jsonify({
        'status': 'success',
        'FILES': FILE_NAMES
    })    
 