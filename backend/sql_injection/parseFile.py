# This file is used for experiment purpose
# generate AST from files that we know for sure is safe, or have vulnerbilities. Used for examination and find pattern
# detail of execution result can be found in Notion Resource.

import ast
import os
import pprint


def get_ast_from_filename(filename):
    file = open(filename)
    astNode = ast.parse(file.read())
    return astNode


def isSqlStatementVunerable(astNode: ast.AST):
    isSafe = False
    if isinstance(astNode, list):
        print("list")
    elif isinstance(astNode, ast.Assign):
        print("assign")
    stringCode = ast.unparse(astNode)
    print(stringCode)

    return isSafe


fileAddressVul1 = "sql_injection_vul1.py"
fileAddressVul2 = "sql_injection_vul2.py"
fileAddressVul3 = "sql_injection_vul3.py"
fileAddressVul4 = "sql_injection_vul4.py"
fileAddressVul5 = "sql_injection_vul5.py"
fileAddressVul6 = "sql_injection_vul6.py"
fileAddressSafe1 = "sql_injection_safe1.py"
fileAddressSafe2 = "sql_injection_safe2.py"

if __name__ == '__main__':
    file = open(fileAddressVul5)

    parsedObj = ast.parse(file.read())
    print(parsedObj.body)
    dumpResult = ast.dump(parsedObj, indent=4)
    print(type(dumpResult))
    print(dumpResult)
