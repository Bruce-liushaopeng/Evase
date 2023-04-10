import os
from flask import Flask, request, make_response, send_file, jsonify

from flask_cors import CORS
import shutil
import threading
import atexit
from pathlib import Path
import json
from typing import Dict
import logging

from backend.controller_logic import perform_analysis, save_code

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app)


class ProjectRepo:

    def __init__(self, uuid: str, dir_path: str, root_path: str, label: str):
        """
        Deletes a temp directory stored in our memory.

        :param uuid: The uid of the source code directory in memory
        :param dir_path: The main directory of the repo
        :param root_path: The root directory of the source code
        :param label: The project label given to this repository (not unique)
        """
        self._uuid = uuid
        self._dirpath = Path(dir_path)
        self._root_path = Path(root_path)
        self._label = label
        self._analyzed = False

    @property
    def uuid(self) -> str:
        """
        Retrieve the unique identifier for the code.

        :return: Repository identifier
        """
        return self._uuid

    @property
    def label(self) -> str:
        """
        Retrieve the label given to the repository.

        :return: Repository label
        """
        return self._label

    @property
    def folder(self) -> Path:
        """
        Retrieve the main folder of the repository.
        Analysis results are output here.

        :return: Repository folder
        """
        return self._dirpath

    @property
    def root(self) -> Path:
        """
        Retrieve the root of the source code for the repository.

        :return: Root of source code
        """
        return self._root_path

    @property
    def analyzed(self) -> bool:
        """
        Retrieve whether the repository has been analyzed or not.

        :return: Analysis status
        """
        return self._analyzed

    def mark(self):
        """
        Marks the status as analyzed.
        """
        self._analyzed = True

    def __str__(self) -> str:
        """
        String representation of the repository.

        :return: String representation
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        String representation of the repository.

        :return: String representation
        """
        return f'REPO({self._uuid}):{self._label}@{self._dirpath}'


def cleanup():
    pass


with app.app_context():
    # internal mapping of project repositories
    ID_REPO_MAPPING: Dict[str, ProjectRepo] = {}
    lock = threading.Lock()
    timers = []
    stop_event = threading.Event()
    atexit.register(cleanup)  # at program exit, allow the remaining code to be purged


def del_tmp(repo: ProjectRepo):
    """
    Deletes a temp directory stored in our memory.

    :param repo: The repository object to delete
    """
    with lock:
        try:
            del ID_REPO_MAPPING[repo.uuid]
            shutil.rmtree(repo.folder, ignore_errors=True)
            logger.info(f"Removal of {repo} was successful.")
        except KeyError:
            logger.critical(f"Removal of {repo} ended in FAILURE.")
            pass


@app.route('/upload/<prj_name>', methods=['POST'])
def file_upload_hook(prj_name: str):
    """
    Hook that is called when the frontend pushes attempts to push a file to backend.
    """

    # parse the JSON arguments from the request.
    est_time = request.args.get("est_time", 30.0)
    try:
        est_time = float(est_time)

    # estimated time not convertible to float
    except:
        response = make_response(jsonify({
            'message': "Couldn't parse the est_time parameter."
        }), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        file = request.files['file']  # get the file from post request

    # file was not passed
    except KeyError:
        response = make_response(jsonify({
            'message': 'Expected file in body (file)'
        }), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    try:
        # attempt a save of the code
        uid, dirpath, subdir_path = save_code(file, prj_name)

        # make the new repository and store in memory
        new_repo = ProjectRepo(uid, dirpath, subdir_path, prj_name)
        with lock:
            ID_REPO_MAPPING[uid] = new_repo

        # schedule repository for deletion
        timer = threading.Timer(est_time, lambda: thread_clean(new_repo))
        timer.daemon = True  # daemon threads to stop when program exits
        timers.append(timer)
        timer.start()
        logger.info(f'{new_repo} scheduled for deletion in {est_time} seconds.')

        response = make_response(jsonify({
            'uuid': uid,
            'message': 'File uploaded successfully'
        }), 201)
        response.headers['Content-Type'] = 'application/json'
        return response

    # value error occurs
    except ValueError as e:
        response = make_response(jsonify({
            'message': str(e)
        }), 422)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/analyze', methods=['POST'])
def analyze_file_hook():
    """
    Analyzes the contents of the code given.
    The code is identified with the uuid argument in the query.
    """

    # parse the JSON arguments from the request.
    try:
        request_body = request.json

        # get the unique identifier
        try:
            uid = request_body['uuid']
            try:
                uid = str(uid)

            # uuid not convertible to string
            except:
                response = make_response(jsonify({
                    'message': "Couldn't parse id from request, it must be either a string or integer."
                }), 400)
                response.headers['Content-Type'] = 'application/json'
                return response
        # uuid not passed at all
        except KeyError:
            response = make_response(jsonify({
                'message': "Couldn't parse id from request, it was not present in the request."
            }), 400)
            response.headers['Content-Type'] = 'application/json'
            return response

        # get force parameter
        # if set to true, the analysis will be performed again from scratch
        try:
            force = request_body['force']
            if not isinstance(force, bool):
                response = make_response(jsonify({
                    'message': "Force parameter was set incorrecly, it must be a boolean."
                }), 400)
                response.headers['Content-Type'] = 'application/json'
                return response
        # force parameter was not passed
        except KeyError:
            force = False
    # request json couldn't be parsed
    except Exception as e:
        response = make_response(jsonify({
            'message': "Couldn't process the request, may not be in JSON form."
        }), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        with lock:
            repo: ProjectRepo = ID_REPO_MAPPING[uid]

        # check if the repository exists on the system
        if repo.folder.exists():

            # if results previously exist extract and send them back
            # force makes the results be regenerated either way
            if repo.analyzed and not force:
                result_path = Path(repo.folder, 'results.json')
                if result_path.exists():
                    with result_path.open("r") as rf:
                        result = json.load(rf)
                    response = make_response(jsonify(result), 200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                else:
                    # if the results couldn't be found, generate them (shouldn't happen)
                    pass

            # if not, perform the analysis and mark the repo as analyzed
            if len(os.listdir(str(repo.root))) > 0:
                result = perform_analysis(
                    str(repo.root),
                    str(repo.folder),
                    project_name=repo.label,
                )
                repo.mark()
                response = make_response(jsonify(result), 200)
                response.headers['Content-Type'] = 'application/json'
                return response

        return make_response({
            'message': "Repository was not previously analyzed, nor could the directory for it be found."
        }, 500)
    # keyerror when uuid not found
    except KeyError:
        response = make_response(jsonify({
            'message': 'Invalid ID, not found.'
        }), 404)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/analysislog', methods=['POST'])
def analysislog_file_hook():
    """
    Retrieves the log of the analysis.
    The code is identified with the uuid argument in the query.
    """

    # parse the JSON arguments from the request.
    try:
        request_body = request.json

        # get the unique identifier
        try:
            uid = request_body['uuid']
            try:
                uid = str(uid)

            # uuid not convertible to string
            except:
                response = make_response(jsonify({
                    'message': "Couldn't parse id from request, it must be either a string or integer."
                }), 400)
                response.headers['Content-Type'] = 'application/json'
                return response
        # uuid not passed at all
        except KeyError:
            response = make_response(jsonify({
                'message': "Couldn't parse id from request, it was not present in the request."
            }), 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    # request json couldn't be parsed
    except Exception as e:
        response = make_response(jsonify({
            'message': "Couldn't process the request, may not be in JSON form."
        }), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

    try:
        repo: ProjectRepo = ID_REPO_MAPPING[uid]

        # check if the repository exists on the system
        if repo.folder.exists():

            # if results previously exist extract and send them back
            # force makes the results be regenerated either way
            if repo.analyzed:
                log_path = Path(repo.folder, 'analysis-log.log')
                if log_path.exists():
                    return send_file(log_path, as_attachment=False, mimetype='text/plain',
                                     download_name='analysis-log.log'), 200
                else:
                    response = make_response(jsonify({
                        'message': "Log file coudn't be found."
                    }), 404)
                    response.headers['Content-Type'] = 'application/json'
                    return response
            else:
                response = make_response(jsonify({
                    'message': "The code has yet to be analyzed."
                }), 400)
                response.headers['Content-Type'] = 'application/json'
                return response

    # keyerror when uuid not found
    except KeyError:
        response = make_response(jsonify({
            'message': 'Invalid ID, not found.'
        }), 404)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/deletecode', methods=['POST'])
def remove_code():
    """
    This endpoint allows the user to delete their repository from the server.
    """

    try:
        # attempt to parse out the uuid
        json = request.json
        try:
            uid = json['uuid']
            try:
                uid = str(uid)

            # uuid isn't convertible to string
            except:
                return make_response({
                    'message': "Couldn't parse id from request, it must be either a string or integer."
                }, 404)

        # uuid was not passed in body
        except KeyError:
            return make_response({
                'message': "Couldn't parse id from request, no id given."
            }, 404)
    # request json couldn't be retrieved
    except Exception:
        return make_response({
            'message': "Couldn't parse id from request, may not be in JSON form."
        }, 404)

    try:
        repo = ID_REPO_MAPPING[uid]
        del_tmp(repo)

        return make_response({
            'message': "Repository was deleted."
        }, 200)

    # keyerror when uuid passed not found
    except KeyError:
        return make_response({
            'message': "The unique identifier given was not found on the server."
        }, 404)
    # other exceptions when the code couldn't be deleted
    except Exception as e:
        return make_response({
            'message': "Couldn't delete the code repository from the server."
        }, 500)


def thread_clean(repo):
    """
    Remove a repository (with a thread).

    :param repo: Repository to delete
    """
    if stop_event.is_set():
        return

    del_tmp(repo)


def cleanup():
    """
    Run upon program termination to delete all remaining files.
    """
    logger.info("Cleanup process began.")

    stop_event.set()  # ensure that callbacks are stopped
    logger.info("Cancelling deletion threads.")
    for timer in timers:
        timer.cancel()

    for uid, repo in ID_REPO_MAPPING.items():
        with lock:
            try:
                shutil.rmtree(repo.folder)
                logger.info(f"Removal of {repo} was successful.")
            except Exception:
                logger.critical(f"Removal of {repo} ended in FAILURE.")
                pass

    ID_REPO_MAPPING.clear()
    atexit.unregister(cleanup)

    for thread in threading.enumerate():
        if thread is not threading.current_thread():
            thread.join()
if __name__ == '__main__':
    # when the BACKEND_PORT is not set(not running with Dcoker), use port 5050
    BACKEND_PORT = os.environ.get('BACKEND_PORT', '5050')
    app.run(debug=True, host='0.0.0.0', port=BACKEND_PORT)
