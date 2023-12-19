import ply.lex as lex

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
        'GENERAL'#TODO: Work on this
    )

    # Regular expression rules for tokens
    #t_KNOWLEDGE_WORLD  = r'K[ps]\s*x[0-9]+\s*&\s*y[0-9]+\n|K[ps]\s*y[0-9]+\s*&\s*x[0-9]+\n'
    t_AND    = r'&'
    t_OR     = r'\|'
    t_BIARROW   = r'='
    t_ARROW  = r'>'
    t_NEG  = r'-'
    t_KNOWLEDGE  = r'K[ps]'
    t_ATOM  = r'[xy][0-9]+'

    # A string containing ignored characters (whitespaces)
    t_ignore  = ' \t'

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

