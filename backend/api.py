import os
from flask import Flask, request, make_response
from flask_cors import CORS
import logging
import shutil
import threading
import atexit

from backend.controller_logic import perform_analysis, save_code

ID_DIR_MAPPING = {}

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

CURR_LOC = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(CURR_LOC, 'user_files')
ANALYSIS_RESULTS_PATH = os.path.join(UPLOAD_FOLDER, 'analysis_results.json')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)


def cleanup():
    """
    Run upon program termination to delete all remaining files.
    """
    for uid, (path, _, _) in ID_DIR_MAPPING.items():
        del_tmp(path, uid)

    ID_DIR_MAPPING.clear()


atexit.register(cleanup)


def del_tmp(file: str, uuid: str):
    """
    Deletes a temp directory stored in our memory.

    :param file: The file path
    :param uuid: The uid of the source code directory in memory
    """
    del ID_DIR_MAPPING[uuid]
    shutil.rmtree(file, ignore_errors=True)


@app.route('/upload/<prj_name>', methods=['POST'])
def file_upload_hook(prj_name: str):
    """
    Hook that is called when the frontend pushes attempts to push a file to backend
    """

    est_time = request.args.get("est_time")
    if est_time is None:
        est_time = 60000.0

    try:
        file = request.files['file']  # get the file from post request
    except KeyError:
        return make_response({
            'message': 'Expected file in body (file)'
        }, 500)

    try:
        uid, dirpath, subdir_path = save_code(file, prj_name)
        ID_DIR_MAPPING[uid] = (dirpath, subdir_path, prj_name)

        print("CHECK", os.path.exists(dirpath))

        timer = threading.Timer(est_time, lambda: del_tmp(dirpath, uid))
        timer.start()

        return make_response({
            'uuid': uid,
            'message': 'File uploaded successfully'
        }, 201)
    except ValueError as e:
        return make_response({
            'message': str(e)
        }, 422)


@app.route('/analyze', methods=['GET'])
def analyze_file_hook():
    """
    Analyzes the contents of the code given.
    The code is identified with the uuid argument in the query.
    """
    uid = request.args.get('uuid')
    if uid is None:
        return make_response({
            'message': 'No ID given'
        }, 404)

    try:
        print("HEREHERE")
        path, subdir, prj_name = ID_DIR_MAPPING[uid]
        print(os.path.exists(path))
        print(subdir)
        if len(os.listdir(subdir)) > 0:
            print("CALLED")

            result = perform_analysis(
                subdir,
                path,
                project_name=prj_name,
            )

            del_tmp(path, uid)

            return make_response(result, 200)

    except KeyError:
        return make_response({
            'message': 'Invalid ID, not found'
        }, 422)
    except Exception as e:
        print(e)
        return make_response({
            'message': 'Unexpected error'
        }, 500)
