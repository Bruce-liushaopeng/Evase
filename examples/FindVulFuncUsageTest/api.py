# import sql_injection_vul5
# import sql_injection_vul5 as vul5
# from sql_injection_vul5 import adminExec
from sql_injection_vul5 import adminExec as myExec
@app.route('/handleAdmin', methods=['POST'])
def handle_admin():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    myExec(username, a, b)

