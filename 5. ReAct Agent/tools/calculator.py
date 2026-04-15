import ast
import operator

# Supported operators mapping
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

def _eval_expr(node):
    """
    Inner recursion to evaluate safe mathematical AST nodes.
    """
    if isinstance(node, ast.Num): # for python < 3.8
        return node.n
    elif isinstance(node, ast.Constant): # python >= 3.8
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_expr(node.left)
        right = _eval_expr(node.right)
        op_func = OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator: {type(node.op)}")
        return op_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_expr(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
        elif isinstance(node.op, ast.UAdd):
            return +operand
        else:
             raise ValueError(f"Unsupported unary operator: {type(node.op)}")
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")

def calculator(expression: str) -> str:
    """
    Safely evaluate math expressions using python's AST.
    """
    try:
        # Using ast.parse to parse the string into an expression node
        node = ast.parse(expression, mode='eval').body
        result = _eval_expr(node)
        return str(result)
    except Exception as e:
        return f"Error: Unable to calculate expression '{expression}'. {str(e)}"
