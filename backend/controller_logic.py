import io

from evase.structures.analysisperformer import AnalysisPerformer
import tempfile
import sched
import os
import zipfile
import time
import uuid
import tarfile

from werkzeug.utils import secure_filename


TEMP_DIR = tempfile.gettempdir()
FILE_DELETION_SCHED = sched.scheduler(time.time, time.sleep)


def perform_analysis(
        folder: str,
        output_folder: str,
        project_name: str = None):
    if project_name is None:
        project_name = "UNKNOWN"

    analysis_performer = AnalysisPerformer(project_name=project_name, project_root=folder)

    analysis_performer.perform_analysis()
    results = analysis_performer.get_results()
    return results


def get_dir_from_uuid(unique_id: str):
    return os.path.join(TEMP_DIR, unique_id)


def save_code(file, label: str, est_time: float):
    filename = secure_filename(file.filename)
    label = secure_filename(label)

    unique_id = str(uuid.uuid4())
    tmp_upload = tempfile.TemporaryDirectory(prefix=f'{label}_{unique_id}_')

    sub_dir_name = str(uuid.uuid4())
    sub_dir_path = os.path.join(tmp_upload.name, sub_dir_name)
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
        tmp_upload.cleanup()
        raise ValueError("File extension was invalid.")