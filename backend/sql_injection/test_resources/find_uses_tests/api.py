from flask import Flask

from test_resources.find_uses_tests.second import lastAPI

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def file_upload_hook(a):
    lastAPI(a)