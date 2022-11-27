from os import *
import sqlite3 as sql3


def amdinExec(username, a, c):
    password, b, c = a+c, c, "2"
    c = "a"+a + c

    cursor = sql3.Cursor()
    cursor.execute("SELECT admin FROM users WHERE username = '" + username+ " here" + password, "h", password)