import string
from os import *
import sqlite3 as sql3


def amdinExec(self, password: string, a: string, c: string):
    b = 4
    d = ""  # [d:{}}]
    g = c  # [{g:{c}, d:{}}]
    if a == 5:
        f = password  # [{g:{c}, d:{}, f:{password}]
        if b == 2:
            d = f  # [{g:{c}, d:{password}, f:{password}]

        # does not go in "if b==2:"
        # {g:{c}, d:{}, f:{password}}

        # does go in "if b==2:"
        # {g:{c}, d:{password}, f:{password}}

        # possible_marked_var_to_params is now
        # [{g:{c}, d:{}, f:{password}}, {g:{c}, d:{password}, f:{password}}]

        f = d  # [{g:{c}, d:{}, f:{}}, {g:{c}, d:{password}, f:{password}}]

    # does not go in "if a==5:"
    # {g:{c}, d:{}}

    # does go in "if a==5:"
    # [{g:{c}, d:{}, f:{}}, {g:{c}, d:{password}, f:{password}]

    # possible_marked_var_to_params is now
    # [ {g:{c}, d:{}}, {g:{c}, d:{}, f:{}}, {g:{c}, d:{password}, f:{password}}]

    cursor = sql3.Cursor()
    cursor.execute("SELECT admin FROM users WHERE username = '" + d, "h", password)

    # d is the only variable present in the dangerous cursor.execute
    # {g:{c}, d:{}}             d is not equal to a parameter -> not dangerous
    # {g:{c}, d:{}, f:{}}       d is not equal to a parameter -> not dangerous
    # {g:{c}, d:{password}, f:{password}}   d is equal to a parameter -> dangerous


def fun():
    amdinExec("a", "b", "c")
