from util.moreutil.helper2 import pretty_print_dict
from util.helper import pretty_print

def main():

    ugly_str = input("Please input an ugly string.")

    pretty_print(ugly_str)

    dct = {
        'no': 1,
        'best': 'tony'
    }

    pretty_print_dict(dct)