from sql_injection_vul5 import adminExec as myCustomName
@app.route('/handleAdmin', methods=['POST'])
def handle_admin():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    adminExec(username, a, b)

