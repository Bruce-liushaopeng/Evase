import ast
import testutil

if __name__ == '__main__':
    import testutil
    r = testutil.vul1_filename
    with open(r, 'r') as f:
        print(ast.parse(f.read()).body[0].decorator_list[0].__dict__)