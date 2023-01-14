from find_uses_tests.sql_injection_vul5 import adminExec as a

def func():
    b = "2"
    a("a",b,"c")
    c = "3"
    a("a",b,"c")
