import parseFile
import ast
from pprint import pprint
from SqlInjectionNodeVisitor import SqlInjectionNodeVisitor
from backend.depanalyze.modulestructure import ModuleAnalysisStruct

ast1 = parseFile.get_ast_from_filename(parseFile.fileAddressVul5)

ma1 = ModuleAnalysisStruct(ast1)
sqlVisitor = SqlInjectionNodeVisitor(parseFile.fileAddressVul5, ma1)

new_ast1 = sqlVisitor.assign_parent_nodes(ast1)

print("Dumping initial AST")
print("==========================")
pprint(ast.dump(new_ast1, indent=2))
print("==========================")

sqlVisitor.visit(ast1)

print("execute are called in the following functions")
print("=====================")
for funcName in sqlVisitor.problemFunctions:
    print(funcName)
