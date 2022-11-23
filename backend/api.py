import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import zipfile
import glob
import shutil
import atexit

UPLOAD_FOLDER = 'user_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# make directory upon startup
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def file_upload_hook():
    """
    Hook that is called when the frontend pushes attempts to push a file to backend
    """
    file = request.files['file']  # get the file from post request
    filename = secure_filename(file.filename)  # get the fileName
    print(filename)

    _, file_extension = os.path.splitext(filename)
    if file_extension != ".zip":  # ensure upload type by checking the last three char
        return "please upload in a zip format"

    if not os.path.exists(UPLOAD_FOLDER):  # create folder if folder doesn't exist
        os.mkdir(UPLOAD_FOLDER)
    destination = os.path.join(UPLOAD_FOLDER, filename)

    file.save(destination)  # save file to the path we defined
    with zipfile.ZipFile(destination, 'r') as zip_ref:  # unzip userfiles
        zip_ref.extractall(UPLOAD_FOLDER)
    os.remove(destination)  # delete the zip file after unziping it
    return "upload successful, check backend folder for User Files"

@app.route('/cancelupload', methods=['DELETE'])
def cancel_upload_hook():
    """
    Hook that is called when the user wants to upload a new file (remove the current).
    """
    if not os.path.exists(UPLOAD_FOLDER):
        return "no file present"
    shutil.rmtree(UPLOAD_FOLDER)
    return "internal directory deleted"



