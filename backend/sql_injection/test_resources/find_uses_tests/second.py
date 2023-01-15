from find_uses_tests.sql_injection_vul5 import adminExec as a

def outside_func(f):
    b = f
    c = "3"
    a(b,b,"c")


def lastAPI():
    a = 1
    outside_func(a)