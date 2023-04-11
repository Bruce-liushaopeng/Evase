import io
import shutil

from evase.structures.analysisperformer import AnalysisPerformer, SQLInjectionBehaviourAnalyzer
import tempfile
import os
import zipfile
import uuid
import tarfile
import json
from pathlib import Path

from werkzeug.utils import secure_filename

def perform_analysis(
        folder: str,
        output_folder: str,
        project_name: str = None
    ) -> dict:
    """
    Performs SQL injection analysis using the EvaseAnalysis package.

    :param folder: The root of the project
    :param output_folder: The location to output results
    :param project_name: The name given to the project
    :return: Results of analysis (currently dict)
    """

    if project_name is None:
        project_name = "UNKNOWN"

    analysis_performer = AnalysisPerformer(project_name=project_name, project_root=folder, output_path=output_folder)
    analysis_performer.strategy = SQLInjectionBehaviourAnalyzer()

    analysis_performer.perform_analysis()
    results = analysis_performer.get_results()

    # attempt to write the file to the temp folder
    try:
        with open(str(Path(output_folder, 'results.json')), "w") as jsonfile:
            jsonfile.write(json.dumps(results))
    except Exception as e:
        pass

    return results


def save_code(file, label: str):
    """
    Service function to save code.

    :param file: The file to save
    :param label: The label to incorporate in the path
    :return: unique ID given, main folder, and inner code folder
    """
    filename = secure_filename(file.filename)
    label = secure_filename(label)

    unique_id = str(uuid.uuid4())
    tmp_upload = tempfile.mkdtemp(prefix=f'{label}_{unique_id}_')

    sub_dir_name = str(uuid.uuid4())
    sub_dir_path = os.path.join(tmp_upload, sub_dir_name)
    _, file_extension = os.path.splitext(filename)

    # ensure upload type
    if file_extension == ".zip":
        with zipfile.ZipFile(file, 'r') as zip_file:
            zip_file.extractall(sub_dir_path)
            return unique_id, tmp_upload, sub_dir_path
    elif file_extension == ".tar":
        with tarfile.open(fileobj=io.BytesIO(file.read())) as tar:
            tar.extractall(sub_dir_path)
            return unique_id, tmp_upload, sub_dir_path
    elif file_extension == ".gz":
        with tarfile.open(fileobj=io.BytesIO(file.read())) as tar:
            tar.extractall(sub_dir_path)
            return unique_id, tmp_upload, sub_dir_path
    else:
        shutil.rmtree(tmp_upload, ignore_errors=True)
        raise ValueError("File extension was invalid.")
