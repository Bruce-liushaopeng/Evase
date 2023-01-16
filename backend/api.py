import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import zipfile
import logging

from backend.controller_logic import perform_analysis

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


@app.route('/analyze', methods=['GET'])
def analyze_file_hook():
    """

    """
    if len(os.listdir(UPLOAD_FOLDER)) > 0:
        # perform analysis here
        print("Begin analysis")
        project_name = request.args.get('prjname', default=None, type=str)
        check_sql_injection = request.args.get('sql', default=False, type=bool)
        check_forced_deadlock = request.args.get('fdl', default=False, type=bool)
        check_no_encryption = request.args.get('nen', default=False, type=bool)
        check_dictionary = request.args.get('dct', default=False, type=bool)

        return perform_analysis(
            UPLOAD_FOLDER,
            project_name=project_name,
            sql_injection=check_sql_injection,
            forced_deadlock=check_forced_deadlock,
            no_encryption=check_no_encryption,
            dictionary=check_dictionary
        )
    else:
        return "No folder was uploaded. Can't perform analysis."

