from searching import *
from analysisutil import *

def get_usage_of_vul_function_test():
    print("get_usage_of_vul_function_test")
    test_path = r"D:\work\programming\Evase\examples\FindVulFuncUsageTest" # replace this string with location of folder containing vulnerable project.
    asts = dir_to_module_structure(test_path)
    get_dependency_relations(test_path, asts)
    get_function_uses(asts, 'adminExec', 'sql_injection_vul5')

def searchCallingTreeTest():
    test_path = r"D:\work\programming\Evase\examples\FindVulFuncUsageTest"
    initialVul = [{
        "function": "adminExec",
        "module": 'sql_injection_vul5'
    }]
    searchCallingTree(test_path, initialVul)

if __name__ == '__main__':
    get_usage_of_vul_function_test()