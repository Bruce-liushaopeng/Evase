import io
import json
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
        #json.dump()
        unique_id = res.json['uuid']
        res = client.post(f'/analyze', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 200

        try:
            print(res)
            json_res = res.json
            assert res.is_json
        except Exception as e:
            pytest.fail(f"Failed to parse response as JSON: {res.get_data(as_text=True)}. Error: {e}")

        assert 'graph' in json_res

        # try the analysis again... file should be ok
        res = client.post(f'/analyze', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 200

        # try to get the analysis log
        res = client.post(f'/analysislog', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 200

        res = client.post(f'/deletecode', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 200

        # AFTER DELETION ALL SHOULD RETURN 404
        res = client.post(f'/deletecode', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 404

        res = client.post(f'/analysislog', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 404

        res = client.post(f'/analyze', data=json.dumps({
            'uuid': unique_id
        }), content_type='application/json')
        assert res.status_code == 404
