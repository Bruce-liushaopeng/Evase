import io
import os
import tempfile

import pytest

import backend.api as api

RES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')


@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True

    with api.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])


def test_file_upload(client):
    """Start with a blank database."""

    with open(os.path.join(RES_PATH, 'demo', 'backend.zip'), 'rb') as file_data:

        test_prj_name = 'EVASE_TEST_UPLOAD'

        data = {}
        data['file'] = (io.BytesIO(file_data.read()), 'backend.zip')
        res = client.post(f'/upload/{test_prj_name}', data=data, content_type='multipart/form-data')

        assert res.is_json

        json_res = res.json
        assert 'uuid' in json_res
        assert 'message' in json_res

def test_file_upload_analyze(client):

    with open(os.path.join(RES_PATH, 'demo', 'backend.zip'), 'rb') as file_data:

        test_prj_name = 'EVASE_TEST_UPLOAD'

        data = {}
        data['file'] = (io.BytesIO(file_data.read()), 'backend.zip')
        res = client.post(f'/upload/{test_prj_name}', data=data, content_type='multipart/form-data')

        unique_id = res.json['uuid']
        res = client.get(f'/analyze?uuid={unique_id}')
        assert res.is_json

        assert 'graph' in res.json

        # try the analysis again... file should be deleted
        res = client.get(f'/analyze?uuid={unique_id}')
        assert res.status_code == 422