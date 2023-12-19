import ply.yacc as yacc
import ply.lex as lex
import re
from logic_lexer import Logic_Lexer
from logic_parser import Logic_Parser

def xSmallerEqual(x: int, y: int):
    return x <= y

def xySumLessEq100(x: int, y: int):
    return x + y <= 100

if __name__ == "__main__":
    # Build the parser
    logic_lexer = Logic_Lexer()
    logic_lexer.build()
    lexer = logic_lexer.lexer
    logic_parser = Logic_Parser()
    logic_parser.build()
    parser = logic_parser.parser
    print(parser.parse("Kp(x4 & y13) | Ks(-Kp(x4 & y13))"), "\n\n\n\n")# Works
    print(parser.parse("Kp(x4 & y13) | Ks-Kp(x4 & y13)"))# Works

    # Combined Test #TODO: Finish this

    x4_and_y13 = re.split(r'\(', parser.parse("x4 & y13"))[0]
    s_knows_p_does_not_know = re.split(r'\(', parser.parse("x4 & y13"))[0]

    model = Kripke_Model(2, 100, [xSmallerEqual, xySumLessEq100])
    print(model.evaluateStatement(x4_and_y13))
    model.publicAnnouncementUpdate(s_knows_p_does_not_know)
    model.publicAnnouncementUpdate(p_knows)
    model.publicAnnouncementUpdate(s_knows)
    print(model.evaluateStatement(x4_and_y13))
    print(model.worlds.keys())