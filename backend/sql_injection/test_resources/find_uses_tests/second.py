from find_uses_tests.sql_injection_vul5 import adminExec as a
import find_uses_tests.sql_injection_vul5 as a
def outside_func(f):
    b = f
    c = "3"
    a.adminExec(b,b,"c")


def lastAPI(a):
    outside_func(a)