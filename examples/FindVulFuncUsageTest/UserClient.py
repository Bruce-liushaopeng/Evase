
import sql_injection_vul5
# Case 1, importing all module

@app.route('/handleAdmin', methods=['POST'])
def handle_admin():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    sql_injection_vul5.adminExec(username, a, b)
