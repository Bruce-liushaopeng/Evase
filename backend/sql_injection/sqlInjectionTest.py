import parseFile
from SqlInjectionNodeVisitor import SqlInjectionNodeVisitor

ast1 = parseFile.get_ast_from_filename(parseFile.fileAddressVul6)

sqlVisitor = SqlInjectionNodeVisitor()

sqlVisitor.visit(ast1)

print("execute are called in the following functions")
print("=====================")
for funcName in sqlVisitor.problemFunctions:
    print(funcName)
