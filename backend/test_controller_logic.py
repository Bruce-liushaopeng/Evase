from backend.controller_logic import perform_analysis
import os


def main():
    path_here = os.path.dirname(os.path.realpath(__file__))
    demo_code = os.path.join(path_here, 'test', 'resources','demo')
    perform_analysis(demo_code,"backend", sql_injection=True)


if __name__ == '__main__':
    main()
