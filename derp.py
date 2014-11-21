"""
141 Tree Lab - Derp the Interpreter

Derp is a simple interpreter that parses and evaluates preorder expressions 
containing basic arithmetic operators (*,//,-,+).  It performs arithmetic with
integer only operands that are either literals or variables (read from a 
symbol table).  It dumps the symbol table, produces the expression infix with 
parentheses to denote order of operation, and evaluates/produces the result of 
the expression.

Author: Sean Strout (sps@cs.rit.edu)

Author: Daniel Roberts
"""

from derp_node import *
    
##############################################################################
# parse
############################################################################## 

def parse(tokens,a):
    """parse: list(String) -> Node, a(List) -> Nodes
    From an infix stream of tokens, construct and return the tree,
    as a collection of Nodes, that represent the expression.
    """

    token = tokens.pop(0)
    
    if token.isdigit():
        a.append(LiteralNode(int(token)))
        token = LiteralNode(int(token))
    elif token.isidentifier():
        a.append(VariableNode(token))
        token = VariableNode(token)
    elif token == '+':
        a.append(AddNode(None,None))
        token = AddNode(None,None)
    elif token == '-':
        a.append(SubtractNode(None,None))
        token = SubtractNode(None,None)
    elif token == 'x' or token == '*':
        a.append(MultiplyNode(None,None))
        token = MultiplyNode(None,None)
    elif token == '//':
        a.append(DivideNode(None,None))
        token = DivideNode(None,None)
    else:
        raise Exception("An error occurred while parsing...")

    if isinstance(token,LiteralNode) or isinstance(token,VariableNode):
        return token
    else:
        token.left = parse(tokens,a)
        token.right = parse(tokens,a)
        return token
    
##############################################################################
# infix
##############################################################################
        
def infix(node):
    """infix: Node -> String | TypeError
    Perform an inorder traversal of the node and return a string that
    represents the infix expression."""

    string = ""

    if isinstance(node,LiteralNode):
        return string + str(node.val)
    elif isinstance(node,VariableNode):
        return string + str(node.name)
    elif isinstance(node,AddNode):
        string = string + infix(node.left) + "+" + infix(node.right)
    elif isinstance(node,MultiplyNode):
        string = string + infix(node.left) + "*" + infix(node.right)
    elif isinstance(node,DivideNode):
        string = string + infix(node.left) + "/" + infix(node.right)
    elif isinstance(node,SubtractNode):
        string = string + infix(node.left) + "-" + infix(node.right)
    else:
        raise Exception("Error while converting to infix...")
    
    return "(" + string + ")"
    
 
##############################################################################
# evaluate
##############################################################################    
      
def evaluate(node, symTbl):
    """evaluate: Node * dict(key=String, value=int) -> int | TypeError
    Given the expression at the node, return the integer result of evaluating
    the node.
    Precondition: all variable names must exist in symTbl"""
    
    result = 0

    if isinstance(node,LiteralNode):
        return result + int(node.val)
    elif isinstance(node,VariableNode):
        return result + int(symTbl[node.name])
    elif isinstance(node,AddNode):
        result += int(evaluate(node.left, symTbl)) + int(evaluate(node.right, symTbl))
    elif isinstance(node,MultiplyNode):
        result += int(evaluate(node.left, symTbl)) * int(evaluate(node.right, symTbl))
    elif isinstance(node,DivideNode):
        result += int(evaluate(node.left, symTbl)) // int(evaluate(node.right, symTbl))
    elif isinstance(node,SubtractNode):
        result += int(evaluate(node.left, symTbl)) - int(evaluate(node.right, symTbl))
    else:
        raise Exception("Error while evaluating...")

    return result
    
##############################################################################
# main
##############################################################################
                     
def main():
    """main: None -> None
    The main program prompts for the symbol table file, and a prefix 
    expression.  It produces the infix expression, and the integer result of
    evaluating the expression"""
    
    print("Hello Herp, welcome to Derp v1.0 :)")
    
    inFile = input("Herp, enter symbol table file: ")

    symTbl = dict()
    dataFile = open(inFile)
    for line in dataFile:
        lst = line.split()
        symTbl[lst[0]] = lst[1]

    print("Symbol Table:",symTbl)   
    print("Herp, enter prefix expressions, e.g.: + 10 20 (RETURN to quit)...")
    
    # input loop prompts for prefix expressions and produces infix version
    # along with its evaluation
    while True:
        prefixExp = input("derp> ")
        if prefixExp == "":
            break
            
        tokens = prefixExp.split()
        root = parse(tokens,[])
        infixExp = infix(root)
        print("Derping the infix expression:",infixExp)
        result = evaluate(root,symTbl)
        print("Derping the evaluation:",result)
         
    print("Goodbye Herp :(")
    
if __name__ == "__main__":
    main()
