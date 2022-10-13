import time
import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import zipfile
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = 'User File'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def fileUpload():
    file = request.files['file']  # get the file from post request
    filename = secure_filename(file.filename)  # get the fileName
    fileExtension = filename[-3:]
    if (fileExtension != "zip"):  # ensure upload type by checking the last three char
        return "please upload in a zip format"
    if not os.path.isdir(UPLOAD_FOLDER):  # create folder if folder doesn't exist
        os.mkdir(UPLOAD_FOLDER)
    destination = "/".join([UPLOAD_FOLDER, filename])
    file.save(destination)  # save file to the path we defined
    with zipfile.ZipFile(destination, 'r') as zip_ref:  # unzip userfiles
        zip_ref.extractall(UPLOAD_FOLDER)
    os.remove(destination)  # delete the zip file after unziping it
    response = "upload successful, check backend folder for User Files"
    return response
