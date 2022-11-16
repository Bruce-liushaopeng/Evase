# from pprint import *

from api.depanalyze.src.test4 import Point2
from api.depanalyze.src.test123.test2 import Point2


def pprint(msg):
    print(msg)


class Point:
    test = []

    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Point.")
        return super().__new__(cls)

    def __init__(self, x, y):
        print("2. Initialize the new instance of Point.")
        self.x = x
        self.y = y

    def build_word_list(self, str):

        pprint(str + " world")
        p = Point2()
        p.helper()

Point(1,3).build_word_list("str")