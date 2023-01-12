# Case 3, funciton using AS
from sql_injection_vul5 import adminExec as myExec

@app.route('/handleAdmin', methods=['POST'])

def otherFunction():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    myExec(username, a, b)

def handle_admin():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    myExec(username, a, b)

