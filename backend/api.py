import os
from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import zipfile
import logging

from backend.controller_logic import perform_analysis

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

CURR_LOC = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(CURR_LOC, 'user_files')
ANALYSIS_RESULTS_PATH = os.path.join(UPLOAD_FOLDER, 'analysis_results.json')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)

PROJECT_NAME = None
PROJECT_FOLDER = UPLOAD_FOLDER

@app.route('/upload/<prj_name>', methods=['POST'])
def file_upload_hook(prj_name: str):
    """
    Hook that is called when the frontend pushes attempts to push a file to backend
    """
    global PROJECT_NAME, PROJECT_FOLDER

    file = request.files['file']  # get the file from post request
    filename = secure_filename(file.filename)  # get the fileName
    print(filename)

    _, file_extension = os.path.splitext(filename)
    if file_extension != ".zip":  # ensure upload type by checking the last three char
        return "please upload in a zip format"

    if not os.path.isdir(UPLOAD_FOLDER):  # create folder if folder doesn't exist
        os.mkdir(UPLOAD_FOLDER)

    upload_dir = os.path.join(UPLOAD_FOLDER, prj_name)
    if not os.path.isdir(upload_dir):  # create folder if folder doesn't exist
        os.mkdir(upload_dir)

    PROJECT_NAME = prj_name
    PROJECT_FOLDER = upload_dir
    destination = os.path.join(upload_dir, filename)

    file.save(destination)  # save file to the path we defined
    with zipfile.ZipFile(destination, 'r') as zip_ref:  # unzip userfiles
        zip_ref.extractall(upload_dir)
    os.remove(destination)  # delete the zip file after unziping it

    response = "upload successful, check backend folder for User Files"
    return response


@app.route('/analyze', methods=['GET'])
def analyze_file_hook():
    """

    """
    global PROJECT_FOLDER
    print("ANALYSIS", PROJECT_FOLDER)
    if len(os.listdir(UPLOAD_FOLDER)) > 0:
        # perform analysis here
        print("Begin analysis")
        check_sql_injection = request.args.get('sql', default=False, type=bool)
        check_forced_deadlock = request.args.get('fdl', default=False, type=bool)
        check_no_encryption = request.args.get('no_enc', default=False, type=bool)
        check_dictionary = request.args.get('pswd_guessing', default=False, type=bool)

        return perform_analysis(
            PROJECT_FOLDER,
            PROJECT_FOLDER,
            project_name=PROJECT_NAME,
            sql_injection=check_sql_injection,
            forced_deadlock=check_forced_deadlock,
            no_encryption=check_no_encryption,
            password_guessing=check_dictionary
        )
    else:
        return "No folder was uploaded. Can't perform analysis."
