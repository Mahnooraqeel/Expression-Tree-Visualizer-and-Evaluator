import operator
from graphviz import Digraph

# Define a tree node
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Helper functions
def is_operator(token):
    return token in {'+', '-', '*', '/', '^'}

def is_operand(token):
    return token.isalnum()  # Alphanumeric operands

# Build expression tree from postfix expression
def build_tree_from_postfix(postfix):
    stack = []
    for token in postfix:
        if is_operand(token):
            stack.append(TreeNode(token))
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression. Not enough operands.")
            node = TreeNode(token) 
            node.right = stack.pop()  # Right operand
            node.left = stack.pop()   # Left operand
            stack.append(node)
        else:
            raise ValueError(f"Invalid token in postfix expression: {token}")
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression. Incorrect number of operands/operators.")
    return stack[-1]

# Build expression tree from prefix expression
def build_tree_from_prefix(prefix):
    stack = []
    for token in reversed(prefix):
        if is_operand(token):
            stack.append(TreeNode(token))
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Invalid prefix expression. Not enough operands.")
            node = TreeNode(token)
            node.left = stack.pop()  # Left operand
            node.right = stack.pop() # Right operand
            stack.append(node)
        else:
            raise ValueError(f"Invalid token in prefix expression: {token}")
    if len(stack) != 1:
        raise ValueError("Invalid prefix expression. Incorrect number of operands/operators.")
    return stack[-1] 

# Convert infix to postfix using Shunting Yard Algorithm
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}
    output = []
    stack = []
    for token in expression:
        if is_operand(token):
            output.append(token)
        elif is_operator(token):
            while (stack and stack[-1] != '(' and
                   (precedence[token] < precedence[stack[-1]] or
                    (precedence[token] == precedence[stack[-1]] and associativity[token] == 'L'))):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            raise ValueError(f"Invalid token in infix expression: {token}")
    while stack:
        output.append(stack.pop())
    return output

# Detect expression type
def detect_expression_type(expression):
    if is_operator(expression[0]):
        return 'prefix'
    elif is_operator(expression[-1]):
        return 'postfix'
    else:
        return 'infix'

# Conversions
def to_infix(node):
    if node is None:
        return ""
    if is_operator(node.value):
        return f"({to_infix(node.left)} {node.value} {to_infix(node.right)})"
    return node.value

def to_postfix(node):
    if node is None:
        return []
    return to_postfix(node.left) + to_postfix(node.right) + [node.value]

def to_prefix(node):
    if node is None:
        return []
    return [node.value] + to_prefix(node.left) + to_prefix(node.right)

# Evaluate expression tree
def evaluate_tree(node):
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow
    }
    if node is None:
        return 0
    if is_operand(node.value):
        try:
            return float(node.value)  # Convert numeric operands
        except ValueError:
            raise ValueError("Cannot evaluate expression with variables.")
    if is_operator(node.value):
        left_value = evaluate_tree(node.left)
        right_value = evaluate_tree(node.right)
        return operations[node.value](left_value, right_value)
    raise ValueError("Invalid node in expression tree.")

# Visualize tree using Graphviz
def visualize_tree_graphviz(node):
    def add_edges(graph, node):
        if node.left:
            graph.edge(str(id(node)), str(id(node.left)))
            add_edges(graph, node.left)
        if node.right:
            graph.edge(str(id(node)), str(id(node.right)))
            add_edges(graph, node.right)

    graph = Digraph(format='png')
    graph.attr('node', shape='circle')

    def add_nodes(graph, node):
        if node:
            graph.node(str(id(node)), node.value)
            add_nodes(graph, node.left)
            add_nodes(graph, node.right)

    add_nodes(graph, node)
    add_edges(graph, node)

    graph.render("expression_tree", view=True)
    print("\nVisualization: Expression tree saved as 'expression_tree.png'.")

# Main program
def main():
    print("\n=== Expression Tree Builder ===\n")
    expression = input("Enter a mathematical expression (tokens separated by spaces): ").split()

    try:
        # Step 1: Detect expression type
        print("\n--- Detecting Expression Type ---")
        expression_type = detect_expression_type(expression)
        print(f"Detected Expression Type: {expression_type.capitalize()}")

        # Step 2: Build tree
        print("\n--- Building Expression Tree ---")
        if expression_type == 'infix':
            postfix = infix_to_postfix(expression)
            tree = build_tree_from_postfix(postfix)
        elif expression_type == 'prefix':
            tree = build_tree_from_prefix(expression)
        elif expression_type == 'postfix':
            tree = build_tree_from_postfix(expression)
        else:
            raise ValueError("Invalid expression type detected.")

        # Step 3: Conversions
        print("\n--- Expression Conversions ---")
        infix = to_infix(tree)
        postfix = to_postfix(tree)
        prefix = to_prefix(tree)
        print(f"Infix Notation   : {infix}")
        print(f"Postfix Notation : {' '.join(postfix)}")
        print(f"Prefix Notation  : {' '.join(prefix)}")

        # Step 4: Evaluation
        print("\n--- Evaluating Expression Tree ---")
        result = evaluate_tree(tree)
        print(f"Evaluated Result : {result:.2f}")

        # Step 5: Visualization
        print("\n--- Visualizing Expression Tree ---")
        visualize_tree_graphviz(tree)

    except ValueError as ve:
        print(f"\nError: {ve}")

    except Exception as e:
        print(f"\nUnexpected Error: {e}")

if __name__ == "__main__":
    main()

# Input Format (Seperated By Spaces): 7 * 8 - 2 / 4