from backend.sql_injection.injectionvisitor import InjectionNodeVisitor
from backend.depanalyze.scoperesolver import ScopeResolver
from testutil import *


def print_execute_funcs(visitor: InjectionNodeVisitor):
    for func_name in visitor.get_execute_funcs():
        print("Execution found in:", func_name)


def get_modulestruct(filename: str):
    tree = get_ast_from_filename(filename)
    return ModuleAnalysisStruct(filename, tree)


def generic_test(filename: str):
    print("Running test for test vulnerability file:", filename)
    visitor = InjectionNodeVisitor()
    ast1 = get_ast_from_filename(filename)
    visitor.visit(ast1)
    print_execute_funcs(visitor)


def test_sql_injection_safe1():
    generic_test(safe1_filename)


def test_sql_injection_safe2():
    generic_test(safe2_filename)


def test_sql_injection_vul1():
    generic_test(vul1_filename)


def test_sql_injection_vul2():
    generic_test(vul2_filename)


def test_sql_injection_vul3():
    generic_test(vul3_filename)


def test_sql_injection_vul4():
    generic_test(vul4_filename)


def test_sql_injection_vul5():
    print("Running test for test vulnerability file:", vul5_filename)
    scoper = ScopeResolver()
    visitor = InjectionNodeVisitor()
    vul5_struct = get_modulestruct(vul5_filename)
    vul5_struct.process(scoper)
    visitor.visit(vul5_struct.get_ast())
    print_execute_funcs(visitor)


def test_sql_injection_vul6():
    generic_test(vul6_filename)


if __name__ == '__main__':
    test_sql_injection_vul5()
