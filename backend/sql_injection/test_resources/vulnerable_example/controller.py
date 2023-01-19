from vulnerable_example.model import check_DB as a
import vulnerable_example.model as a


def check_DB(f):
    b = f
    c = "3"
    a.adminExec(b, b, "c")


def check_DB_wrapper(a):
    check_DB(a)
