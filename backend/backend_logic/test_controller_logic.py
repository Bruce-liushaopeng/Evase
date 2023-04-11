from backend_logic.controller_logic import perform_analysis
import os


def main():
    path_here = os.path.dirname(os.path.realpath(__file__))
    demo_code = os.path.join(path_here, 'test', 'resources', 'demo', 'backend')
    demo_out = os.path.join(path_here, 'test', 'resources', 'demo')
    perform_analysis(demo_code, demo_out)


if __name__ == '__main__':
    main()
