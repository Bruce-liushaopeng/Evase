import parseFile
from injectionvisitor import InjectionNodeVisitor
from backend.depanalyze.scoperesolver import ScopeResolver
from injectionutil import SqlMarker


def print_execute_funcs(visitor: InjectionNodeVisitor):
    for func_name in visitor.get_execute_funcs():
        print("Execution found in:", func_name)


def generic_test(filename: str):
    print("Running test for test vulnerability file:", filename)
    visitor = InjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_safe1():
    generic_test(parseFile.safe1_filename)


def test_sql_injection_safe2():
    generic_test(parseFile.safe2_filename)


def test_sql_injection_vul1():
    generic_test(parseFile.vul1_filename)


def test_sql_injection_vul2():
    generic_test(parseFile.vul2_filename)


def test_sql_injection_vul3():
    generic_test(parseFile.vul3_filename)


def test_sql_injection_vul4():
    generic_test(parseFile.vul4_filename)


def test_sql_injection_vul5():
    print("Running test for test vulnerability file:", parseFile.vul5_filename)
    scoper = ScopeResolver()
    visitor = InjectionNodeVisitor()
    ast1 = parseFile.get_ast_from_filename(parseFile.vul5_filename)
    scoper.visit(ast1)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_vul6():
    generic_test(parseFile.vul6_filename)


if __name__ == '__main__':
    test_sql_injection_vul5()
