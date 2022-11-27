from os import *
import sqlite3 as sql3


def amdinExec(username, a, c):
    password, b, c = "hey", "1", "2"
    c, a = ("a","b")
    c, a = ["a","b"]
    c = "a"

    cursor = sql3.Cursor()
    cursor.execute("SELECT admin FROM users WHERE username = '" + username+ " here" + password, "h", password)