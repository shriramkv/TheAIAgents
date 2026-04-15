"""
Calculator tool for math operations.
"""
import ast
import operator

# Supported operators for safe eval
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def eval_expr(node):
    """
    Safely evaluate an AST math expression node.
    """
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return OPS[type(node.op)](eval_expr(node.left), eval_expr(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return OPS[type(node.op)](eval_expr(node.operand))
    else:
        raise TypeError(f"Unsupported mathematical operation: {type(node)}")

def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression safely.
    
    Args:
        expression (str): The math expression to evaluate.
        
    Returns:
        str: The result of the evaluation.
    """
    try:
        # Evaluating the expression using AST for safety
        node = ast.parse(expression, mode='eval').body
        result = eval_expr(node)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
