import parseFile
from SqlInjectionNodeVisitor import SqlInjectionNodeVisitor


def print_execute_funcs(visitor: SqlInjectionNodeVisitor):
    for func_name in visitor.get_execute_funcs():
        print("Execution found in:", func_name)


def test_sql_injection_safe1():
    print("Running test for test vulnerability file:", parseFile.safe1_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.safe1_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)

def test_sql_injection_safe2():
    print("Running test for test vulnerability file:", parseFile.safe2_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.safe2_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul1():
    print("Running test for test vulnerability file:", parseFile.vul1_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul1_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul2():
    print("Running test for test vulnerability file:", parseFile.vul2_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul2_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul3():
    print("Running test for test vulnerability file:", parseFile.vul3_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul3_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul4():
    print("Running test for test vulnerability file:", parseFile.vul5_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul4_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul5():
    print("Running test for test vulnerability file:", parseFile.vul5_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul5_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul6():
    print("Running test for test vulnerability file:", parseFile.vul6_filename)
    visitor = SqlInjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul6_filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


if __name__ == '__main__':
    test_sql_injection_vul5()
