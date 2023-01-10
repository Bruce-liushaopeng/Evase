from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from injectionvisitor import InjectionNodeVisitor
from backend.depanalyze.scoperesolver import ScopeResolver
import ast
import injectionutil

safe1_filename = 'test_resources/sql_injection_safe1.py'
safe2_filename = 'test_resources/sql_injection_safe2.py'
vul1_filename = 'test_resources/sql_injection_vul1.py'
vul2_filename = 'test_resources/sql_injection_vul2.py'
vul3_filename = 'test_resources/sql_injection_vul3.py'
vul4_filename = 'test_resources/sql_injection_vul4.py'
vul5_filename = 'test_resources/sql_injection_vul5.py'
vul6_filename = 'test_resources/sql_injection_vul6.py'


def get_ast_from_filename(filename: str):
    with open(filename, "r") as af:
        return ast.parse(af.read())


safe1_struct = ModuleAnalysisStruct(safe1_filename, get_ast_from_filename(safe1_filename))
safe2_struct = ModuleAnalysisStruct(safe2_filename, get_ast_from_filename(safe2_filename))
vul1_struct = ModuleAnalysisStruct(vul1_filename, get_ast_from_filename(vul1_filename))
vul1_struct = ModuleAnalysisStruct(vul1_filename, get_ast_from_filename(vul2_filename))
vul1_struct = ModuleAnalysisStruct(vul1_filename, get_ast_from_filename(vul3_filename))
vul1_struct = ModuleAnalysisStruct(vul1_filename, get_ast_from_filename(vul4_filename))


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
    scoper.visit(vul5_struct.get_ast())
    visitor.visit(vul5_struct.get_ast())
    print_execute_funcs(visitor)


def test_sql_injection_vul6():
    generic_test(vul6_filename)

def test_get_all_vars():
    astVul5 = get_ast_from_filename(vul5_filename)
    allVars = injectionutil.get_all_vars(astVul5)
    print(allVars)


if __name__ == '__main__':
    test_get_all_vars()
