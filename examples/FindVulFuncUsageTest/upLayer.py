import sql_injection_vul5 as myVul
# Case 4, entire module imported using as

@app.route('/handleAdmin', methods=['POST'])
def handle_admin():
    username = 'test_user_name'
    a = 'samle_a'
    b = 'sample_b'
    myVul.adminExec(username, a, b)
