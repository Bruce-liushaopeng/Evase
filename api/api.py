import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import zipfile
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = 'user_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

    if not os.path.isdir(UPLOAD_FOLDER):  # create folder if folder doesn't exist
        os.mkdir(UPLOAD_FOLDER)
    destination = os.path.join(UPLOAD_FOLDER, filename)

    file.save(destination)  # save file to the path we defined
    with zipfile.ZipFile(destination, 'r') as zip_ref:  # unzip userfiles
        zip_ref.extractall(UPLOAD_FOLDER)
    os.remove(destination)  # delete the zip file after unziping it
    response = "upload successful, check backend folder for User Files"
    return response
