import ply.yacc as yacc
import ply.lex as lex
from logic_lexer import Logic_Lexer

# Used to translate logic statements to python functions
class Logic_Parser(object):

    def __init__(self):
        self.funcNum = 0
        self.tokens = Logic_Lexer.tokens

    # Show if operators are left or right associated 
    # Further linewise ordered from least restrictive to most 
    precedence = (
        ('left', 'AND', 'OR', 'ARROW', 'BIARROW'),
        ('left', 'KNOWLEDGE', 'KNOWLEDGE_EVERYONE'),
        ('right', 'NEG'),
    )

    # Returns a python function that returns a boolean and accepts a world and a dictionary of worlds
    def p_function(self, p):
        'function : formula'
        function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn" + p[1]
        self.funcNum += 1
        exec(function, globals())
        p[0] = globals()["generatedFunctionName" + str(self.funcNum - 1)]

    # Will be called if the rule applies and will further the construction of the python function (same for the rest of the functions)
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

    # For this problem all atoms are the numbers being a specific number
    def p_formula_atom(self, p):
        'formula : ATOM'
        p[0] = " world." + p[1][0] + " == " + p[1][1: ]

    def p_formula_paranthesis(self, p):
        '''formula : '(' formula ')' '''
        p[0] = " (" + p[2] + ")"

    def p_formula_knowledge_general_atom_and(self, p):
        '''formula : KNOWLEDGE '(' GENERAL_ATOM AND GENERAL_ATOM ')' '''
        assert p[3] != p[5]; "Syntax Error! Sentences with the same generic atoms are not allowed. For example this is not allowed: Kp ( x & x )"
        function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn len(world.relations_"
        if p[1][1] == 'p':
            function += "P) <= 1"
        else:
            function += "S) <= 1"
        p[0] = " generatedFunctionName" + str(self.funcNum) + "(world, worlds)"
        self.funcNum += 1
        exec(function, globals())

    # This is probably a useless rule as given the rules of the riddle if one of the agents knows x or y then they know the other as they also know either the sum and product
    def p_formula_knowledge_general_atom(self, p):
        '''formula : KNOWLEDGE GENERAL_ATOM '''
        function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\tfor worldCoords in world.relations_"
        if p[1][1] == 'p':
            function += "P:"
        else:
            function += "S:"
        function += "\n\t\tif worlds[worldCoords]." + p[2] + " == world." + p[2] + ":"
        function += "\n\t\t\treturn False"
        function += "\n\treturn True"
        p[0] = " generatedFunctionName" + str(self.funcNum) + "(world, worlds)"
        self.funcNum += 1
        exec(function, globals())

    def p_formula_knowledge(self, p):
        '''formula : KNOWLEDGE formula '''
        preFunction = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn" + p[2]
        self.funcNum += 1
        exec(preFunction, globals())
        
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
        exec(function, globals())

    def p_formula_knowledge_everyone(self, p):
        '''formula : KNOWLEDGE_EVERYONE formula '''
        preFunction = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\treturn" + p[2]
        self.funcNum += 1
        exec(preFunction, globals())
        
        function = "def generatedFunctionName" + str(self.funcNum) + "(world, worlds):\n\tfor worldCoords in world.relations_P:" 
        function += "\n\t\tif not generatedFunctionName" + str(self.funcNum - 1) + "(worlds[worldCoords], worlds):"
        function += "\n\t\t\treturn False"

        function += "\n\tfor worldCoords in world.relations_S:"
        function += "\n\t\tif not generatedFunctionName" + str(self.funcNum - 1) + "(worlds[worldCoords], worlds):"
        function += "\n\t\t\treturn False"
        function += "\n\treturn True"
        p[0] = " generatedFunctionName" + str(self.funcNum) + "(world, worlds)"
        self.funcNum += 1
        exec(function, globals())

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")
    
    # Builds the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

