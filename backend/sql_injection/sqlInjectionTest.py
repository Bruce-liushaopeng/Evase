import parseFile
from SqlInjectionNodeVisitor import SqlInjectionNodeVisitor

ast1 = parseFile.get_ast_from_filename(parseFile.fileAddressVul4)

sqlVisitor = SqlInjectionNodeVisitor()

sqlVisitor.visit(ast1)
