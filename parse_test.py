import ply.yacc as yacc
import ply.lex as lex
import re
from model import Kripke_Model
from logic_lexer import Logic_Lexer
from logic_parser import Logic_Parser
from logic_parser import *

def xSmallerEqual(x: int, y: int):
    return x <= y

def xySumLessEq100(x: int, y: int):
    return x + y <= 125

if __name__ == "__main__":
    # Build the parser
    logic_lexer = Logic_Lexer()
    logic_lexer.build()
    lexer = logic_lexer.lexer
    logic_parser = Logic_Parser()
    logic_parser.build()
    parser = logic_parser.parser
    #print(parser.parse("Kp(x4 & y13) | Ks(-Kp(x4 & y13))"), "\n\n\n\n")# Works
    #print(parser.parse("Kp(x4 & y13) | Ks-Kp(x4 & y13)"))# Works

    # Combined Test (Works)

    # This displays the example of the original Sum and Product riddle
    # Public Announcement can be any logic statement without common knowledge 
    # - is negation; > is the arrow; = is the bidirectional arrow; & is and; | is or
    # p and s are the agents; Knowledge operators have a capital K followed by the letter of the agent e.g. Kp
    # x and y are the two numbers Kpx means that p nows the value of x
    # x14 or y14 indicate that the repective variable has that value
    model = Kripke_Model(2, 100, [xSmallerEqual, xySumLessEq100])
    model.publicAnnouncementUpdate(parser.parse("Ks-Kp(x & y)")) # S knows that P does not know x and y
    model.publicAnnouncementUpdate(parser.parse("Kp(x & y)")) # P knows x and y
    model.publicAnnouncementUpdate(parser.parse("Ks(x & y)")) # S knows x and y
    print(model.evaluateStatement(parser.parse("x4 & y13"))) # Evaluate whether the statement is true
    print(model.worlds.keys()) # Display all worlds that are considered