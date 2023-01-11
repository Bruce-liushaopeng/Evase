from os import *
import sqlite3 as sql3


def adminExec(username, a, c):
    password, c, c = a, c, "2"
    c = "a"+a + c

    cursor = sql3.Cursor()
    cursor.execute("SELECT admin FROM users WHERE username = '" + username+ " here" + password, "h", password)


def testUseOfAdminExec():
    adminExec(a, b, c)