import ply.lex as lex

# Tokenizes the input, which can then be used by the parser
class Logic_Lexer(object):
    literals = [ '(',')' ]

    # List of token names.
    tokens = (
        'ATOM',
        'AND',
        'OR',
        'NEG',
        'ARROW',
        'BIARROW',
        'KNOWLEDGE',
        'GENERAL_ATOM'
    )

    # Regular expression rules for tokens
    t_AND    = r'&'
    t_OR     = r'\|'
    t_BIARROW   = r'='
    t_ARROW  = r'>'
    t_NEG  = r'-'
    t_KNOWLEDGE  = r'K[ps]'
    t_ATOM  = r'[xy][0-9]+'
    t_GENERAL_ATOM = r'[xy]'

    # A string containing ignored characters (whitespaces)
    t_ignore  = ' \t'

    # Used to create the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

