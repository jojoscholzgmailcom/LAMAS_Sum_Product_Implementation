import ply.yacc as yacc
import ply.lex as lex
from logic_lexer import Logic_Lexer

class Logic_Parser(object):

    def __init__(self):
        self.funcNum = 0
        self.tokens = Logic_Lexer.tokens

    precedence = (
        ('left', 'AND', 'OR', 'ARROW', 'BIARROW'),
        ('left', 'KNOWLEDGE'),
        ('right', 'NEG'),
    )

    def p_function(self, p):
        'function : formula'
        p[0] = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn" + p[1]
        self.funcNum += 1
        exec(p[0])

    #def p_formula_knowledge_world(self, p):
    #    'formula : KNOWLEDGE_WORLD'
    #    function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn " 
    #    if p[1][1] == 'p':
    #        function += "len(world.relations_P) <= 1"
    #    else:
    #        function += "len(world.relations_S) <= 1"
    #    p[0] = " generatedFunctionName" + str(self.funcNum) + "(world, worlds)"
    #    self.funcNum += 1
    #    print(function, "\n\n")
    #    exec(function)

    def p_formula_and(self, p):
        'formula : formula AND formula'
        p[0] = " " + p[1] + " and" + p[3]

    def p_formula_or(self, p):
        'formula : formula OR formula'
        p[0] = " " + p[1] + " or" + p[3]

    def p_formula_not(self, p):
        'formula : NEG formula'
        p[0] = " not" + p[2]

    def p_formula_arrow(self, p):
        'formula : formula ARROW formula'
        p[0] = " not" + p[1] + " or " + p[3]

    def p_formula_biarrow(self, p):
        'formula : formula BIARROW formula'
        p[0] = " (not" + p[1] + " or " + p[3] + ") and (" + "(" + p[1] + " or not" + p[3] + ")"

    def p_formula_atom(self, p):
        'formula : ATOM'
        p[0] = " world." + p[1][0] + " == " + p[1][1: ]

    def p_formula_paranthesis(self, p):
        '''formula : '(' formula ')' '''
        p[0] = " (" + p[2] + ")"

    def p_formula_knowledge(self, p):
        '''formula : KNOWLEDGE formula '''
        preFunction = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn" + p[2]
        self.funcNum += 1
        exec(preFunction)

        function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\tfor worldCoords in world.relations_" 
        if p[1][1] == 'p':
            function += "P:"
        else:
            function += "S:"
        function += "\n\t\tif not generatedFunctionName" + str(self.funcNum - 1) + "(worlds[worldCoords], worlds):"
        function += "\n\t\t\treturn False"
        function += "\n\treturn True"
        p[0] = " generatedFunctionName" + str(self.funcNum) + "(world, worlds)"
        self.funcNum += 1
        exec(function)

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

