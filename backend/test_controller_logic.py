from backend.api import UPLOAD_FOLDER
from backend.controller_logic import perform_analysis


def main():

    perform_analysis(r"C:\courses\SYSC_4907\Evase\backend\test\resources", r"C:\courses\SYSC_4907\Evase\backend\test\resources", sql_injection=True)

if __name__ == '__main__':
    main()