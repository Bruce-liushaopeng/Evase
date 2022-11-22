from os import *
import sqlite3 as sql3


def amdinExec(username):
    cursor = sql3.Cursor()
    cursor.execute("SELECT admin FROM users WHERE username = '" + username)
