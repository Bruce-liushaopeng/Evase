# This file is used for experiment purpose
# generate AST from files that we know for sure is safe, or have vulnerbilities. Used for examination and find pattern
# detail of execution result can be found in Notion Resource.

import ast
import os
import pprint
os.listdir("./")
fileAddressVul1 = "sql_injection_vul1.py"
fileAddressVul2 = "./sql_injection_vul2.py"
fileAddressVul3 = "./sql_injection_vul3.py"
fileAddressVul4 = "./sql_injection_vul4.py"
fileAddressSafe1 = "sql_injection_safe1.py"
fileAddressSafe2 = "sql_injection_safe2.py"
file = open(fileAddressVul4)

parsedObj = ast.parse(file.read())
print(parsedObj.body)
dumpResult = ast.dump(parsedObj, indent=4)
print(type(dumpResult))
print(dumpResult)
