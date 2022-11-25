# This file is used for experiment purpose
# generate AST from files that we know for sure is safe, or have vulnerbilities. Used for examination and find pattern
# detail of execution result can be found in Notion Resource.

import ast
import re
from typing import Tuple

vul1_filename = "sql_injection_vul1.py"
vul2_filename = "sql_injection_vul2.py"
vul3_filename = "sql_injection_vul3.py"
vul4_filename = "sql_injection_vul4.py"
vul5_filename = "sql_injection_vul5.py"
vul6_filename = "sql_injection_vul6.py"
safe1_filename = "sql_injection_safe1.py"
safe2_filename = "sql_injection_safe2.py"


def get_ast_from_filename(filepath) -> ast.AST:
    """
    Read in filename to ast.
    Assumes filename is a valid Python file.

    :param filepath: path to file
    :return: ast tree of file
    """
    with open(filepath, "r") as f:
        return ast.parse(f.read())
def does_query_match(query: ast.AST):
    """
    =(\s+)?('"|'")(\s+)?\+(\s+)?(\w+)(\s+)?\+(\s+)?('"|'")

    :param query:
    :return:
    """
    query_str = ast.unparse(query)

    print()


def is_query_vulnerable(execute_args) -> Tuple[ast.AST, ...]:
    """
    Determine if the arguments of a query are DIRECTLY arguments.

    Execute arguments is in the form of a list of arguments to a Expr() AST node.
    args=[
        BinOp(
            left=Constant(value="SELECT admin FROM users WHERE username = '"),
            op=Add(),
            right=Name(id='username', ctx=Load()))],
    keywords=[]))]

    Execute arguments should also be in the form of a Return node, and Assign node.

    Return node form:
    def get_query(username: str):
        return "SELECT admin FROM users WHERE username = '" + username

    Assign node form:
    def execute_query():
        query = "SELECT admin FROM users WHERE username = '" + username
        ...

    This function DOESN'T:
    - Detect where arguments inside the query come from

    Return type should be rethought.

    :param execute_args: Query arguments
    :return: The problematic node in the query
    """
    problem_node = None
    if isinstance(execute_args, list):
        print("list represents function arguments")
        if len(execute_args) == 1:
            exec_arg = execute_args[0]
            if isinstance(exec_arg, ast.Name):
                print("case not really handled")
            elif isinstance(exec_arg, ast.BinOp):
                print("binary operator detected")
                if isinstance(exec_arg.op, ast.Mod):
                    print("modulo operator detected")
                    if isinstance(exec_arg.right, ast.Name):
                        problem_node = exec_arg.left, exec_arg.right
                elif isinstance(exec_arg.op, ast.Add):
                    print("add operator detected")
                    if isinstance(exec_arg.right, ast.Name):
                        problem_node = exec_arg.left, exec_arg.right

    elif isinstance(execute_args, ast.Assign):
        print("assign")

    elif isinstance(execute_args, ast.Return):
        # should be the same procedure as the list case of arguments, can't be an assign
        return is_query_vulnerable([execute_args.value])

    string_code = ast.unparse(execute_args)
    print(string_code)

    return problem_node
