from analysisutil import *
from pprint import pprint
import ast

def get_usage_of_vul_function_test():
    print("get_usage_of_vul_function_test")
    bruce_test_path = r"D:\work\programming\Evase\examples\FindVulFuncUsageTest" # replace this string with location of folder containing vulnerable project.
    asts = dir_to_module_structure(bruce_test_path)
    get_dependency_relations(bruce_test_path, asts)
    get_function_uses(asts, 'adminExec', 'sql_injection_vul5')


if __name__ == '__main__':
    get_usage_of_vul_function_test()
    print("ast")
    filepath = r"D:\work\programming\Evase\examples\FindVulFuncUsageTest\api.py"